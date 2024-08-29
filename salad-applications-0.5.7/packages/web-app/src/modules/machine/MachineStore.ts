import { AxiosInstance, AxiosResponse } from 'axios'
import { autorun, computed, flow, observable } from 'mobx'
import { v4 as uuidv4 } from 'uuid'
import { FeatureManager } from '../../FeatureManager'
import * as Storage from '../../Storage'
import { RootStore } from '../../Store'
import { NotificationMessageCategory } from '../notifications/models'
import { getPluginDefinitions } from '../salad-bowl/definitions'
import {
  Accounts,
  BEAM_WALLET_ADDRESS,
  ETH_WALLET_ADDRESS,
  getNiceHashMiningAddress,
  PROHASHING_USERNAME,
} from '../salad-bowl/definitions/accounts'
import { GpuInformation, MachineInfo } from './models'
import { Machine } from './models/Machine'

const SYSTEM_ID = 'SYSTEM_UUID'

export class MachineStore {
  @observable
  public currentMachine?: Machine

  @computed
  get minerId(): string | undefined {
    if (this.store.machine.currentMachine !== undefined) {
      return this.store.machine.currentMachine.minerId
    } else {
      return undefined
    }
  }

  constructor(
    private readonly store: RootStore,
    private readonly axios: AxiosInstance,
    private readonly featureManager: FeatureManager,
  ) {
    autorun(async () => {
      if (!store.auth.isAuthenticated) {
        return
      }

      if (!store.native.machineInfo) {
        return
      }

      if (store.saladBowl.saladBowlConnected === undefined) {
        return
      }

      await this.registerMachine()
    })
  }

  registerMachine = flow(
    function* (this: MachineStore) {
      const machineInfo = this.store.native.machineInfo
      if (!machineInfo) {
        console.warn('No valid machine info found. Unable to register.')
        return
      }

      const { services: _, processes, ...machineWithoutServices } = machineInfo
      if (machineWithoutServices.system != null) {
        machineWithoutServices.system.uuid = Storage.getOrSetDefault(SYSTEM_ID, uuidv4())
      }

      try {
        console.log('Registering machine with salad')
        let res: AxiosResponse<Machine> = yield this.axios.post(`/api/v2/machines`, {
          systemInfo: machineWithoutServices,
        })
        this.currentMachine = res.data

        this.store.analytics.trackMachineInformation(machineInfo)

        if (!this.store.saladBowl.canRun) {
          //Show an error notification
          this.store.notifications.sendNotification({
            category: NotificationMessageCategory.MachineIncompatible,
            title: `Machine is Incompatible`,
            message: 'Salad was unable to detect a compatible graphics card. Click here for more details.',
            autoClose: false,
            type: 'error',
            onClick: () => this.store.routing.push('/earn/mine/miner-details'),
          })
        }
      } catch (err) {
        this.store.analytics.captureException(new Error(`register-machine error: ${err}`), {
          contexts: {
            machineInfo: machineWithoutServices as Record<string, unknown>,
          },
        })
        throw err
      }
    }.bind(this),
  )

  @computed
  get gpus(): GpuInformation[] {
    const machine = this.currentMachine
    const machineInfo = this.store.native.machineInfo
    if (
      machine === undefined ||
      machineInfo?.graphics?.controllers === undefined ||
      machineInfo?.graphics?.displays === undefined
    ) {
      return []
    }

    // TODO: Use an existing copy of the plugin definition list generated by Salad Bowl.
    const accounts: Accounts = {
      ethermine: {
        address: ETH_WALLET_ADDRESS,
        workerId: machine.minerId,
      },
      flypoolBeam: {
        address: BEAM_WALLET_ADDRESS,
        workerId: machine.minerId,
      },
      nicehash: {
        address: getNiceHashMiningAddress(machine.id),
        rigId: machine.minerId,
      },
      prohashing: {
        username: PROHASHING_USERNAME,
        workerName: machine.id,
      },
    }
    const pluginDefinitions = getPluginDefinitions(accounts, machineInfo.platform ?? window.salad.platform)
    const gpus = machineInfo.graphics.controllers.map((gpu) => {
      const gpuMachineInfo: MachineInfo = {
        ...machineInfo,
        graphics: {
          ...machineInfo.graphics!,
          controllers: [gpu],
        },
      }

      // TODO: Feed user preferences into the requirements check.
      const gpuPluginDefinitions = pluginDefinitions.filter((pluginDefinition) =>
        pluginDefinition.requirements.every((requirement) =>
          requirement(
            gpuMachineInfo,
            { cpu: false, gpu: true, cpuOverridden: false, gpuOverridden: false },
            this.featureManager,
          ),
        ),
      )

      return {
        model: gpu.model,
        vram: gpu.memoryTotal || gpu.vram || 0,
        driverVersion: gpu.driverVersion,
        compatible: gpuPluginDefinitions.length > 0,
      }
    })

    return gpus || []
  }

  @computed
  get cpuCompatible(): boolean {
    const machine = this.currentMachine
    const machineInfo = this.store.native.machineInfo
    if (
      machine === undefined ||
      machineInfo?.cpu?.brand === undefined ||
      machineInfo?.memLayout === undefined ||
      machineInfo?.memLayout?.length === 0
    ) {
      return false
    }

    // TODO: Use an existing copy of the plugin definition list generated by Salad Bowl.
    const accounts: Accounts = {
      ethermine: {
        address: ETH_WALLET_ADDRESS,
        workerId: machine.minerId,
      },
      flypoolBeam: {
        address: BEAM_WALLET_ADDRESS,
        workerId: machine.minerId,
      },
      nicehash: {
        address: getNiceHashMiningAddress(machine.id),
        rigId: machine.minerId,
      },
      prohashing: {
        username: PROHASHING_USERNAME,
        workerName: machine.id,
      },
    }
    const pluginDefinitions = getPluginDefinitions(accounts, machineInfo.platform ?? window.salad.platform)

    //Get all the CPU only plugin definitions
    const cpuPlugins = pluginDefinitions.filter((pluginDefinition) =>
      pluginDefinition.requirements.every((requirement) =>
        requirement(
          machineInfo,
          { cpu: true, gpu: false, cpuOverridden: false, gpuOverridden: false },
          this.featureManager,
        ),
      ),
    )

    return cpuPlugins.length > 0
  }
}
