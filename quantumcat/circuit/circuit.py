# (C) Copyright Artificial Brain 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from quantumcat.circuit.op_type import OpType
from quantumcat.exceptions import CircuitError, APIDetailsNotFoundError
from quantumcat.utils import ErrorMessages
from quantumcat.circuit import convert
from quantumcat.utils import providers
from quantumcat.utils import constants
from quantumcat.circuit import execute_circuit
import matplotlib.pyplot as plt
import numpy as np


class QCircuit:
    """docstring for Circuit."""

    def __init__(self, qubits, provider=providers.DEFAULT_PROVIDER):
        super(QCircuit, self).__init__()
        self.qubits = qubits
        self.operations = []
        self.converted_q_circuit = None
        self.provider = provider

    def x_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.x_gate: [qubit]})
        return self

    def y_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.y_gate: [qubit]})
        return self

    def z_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.z_gate: [qubit]})
        return self

    def h_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.h_gate: [qubit]})
        return self

    def cx_gate(self, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.cx_gate: [[control_qubit], [target_qubit]]})
        return self

    def cz_gate(self, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.operations.append({OpType.cz_gate: [[control_qubit], [target_qubit]]})
        return self

    def ccx_gate(self, control_qubit1, control_qubit2, target_qubit):
        self.check_qubit_boundary(control_qubit1)
        self.check_qubit_boundary(control_qubit2)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.ccx_gate: [[control_qubit1], [control_qubit2], [target_qubit]]})
        return self

    def ry_gate(self, theta, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.ry_gate: [qubit],
                                constants.PARAMS: [theta]})
        return self

    def ryy_gate(self, theta, qubit1, qubit2):
        self.check_qubit_boundary(qubit1)
        self.check_qubit_boundary(qubit2)
        self.operations.append({OpType.ryy_gate: [[qubit1], [qubit2]],
                                constants.PARAMS: [theta]})
        return self

    def rzz_gate(self, theta, qubit1, qubit2):
        self.check_qubit_boundary(qubit1)
        self.check_qubit_boundary(qubit2)
        self.operations.append({OpType.rzz_gate: [[qubit1], [qubit2]],
                                constants.PARAMS: [theta]})
        return self

    def rzx_gate(self, theta, qubit1, qubit2):
        self.check_qubit_boundary(qubit1)
        self.check_qubit_boundary(qubit2)
        self.operations.append({OpType.rzx_gate: [[qubit1], [qubit2]],
                                constants.PARAMS: [theta]})
        return self

    def rz_gate(self, phi, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.rz_gate: [qubit],
                                constants.PARAMS: [phi]})
        return self

    # Couldn't file class to map ecr gates in gates_map.py
    # def ecr_gate(self, qubit1, qubit2):
    #     self.check_qubit_boundary(qubit1)
    #     self.check_qubit_boundary(qubit2)
    #     self.operations.append({OpType.ecr_gate: [[qubit1], [qubit2]]})

    def s_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.s_gate: [qubit]})
        return self

    def sdg_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.sdg_gate: [qubit]})
        return self

    def swap_gate(self, qubit1, qubit2):
        self.check_qubit_boundary(qubit1)
        self.check_qubit_boundary(qubit2)
        self.operations.append(({OpType.swap_gate: [[qubit1], [qubit2]]}))
        return self

    def iswap_gate(self, qubit_a, qubit_b):
        self.check_qubit_boundary(qubit_a)
        self.check_qubit_boundary(qubit_b)
        self.operations.append(({OpType.iswap_gate: [[qubit_a], [qubit_b]]}))
        return self

    def sx_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.sx_gate: [qubit]})
        return self

    def sxd_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.sxd_gate: [qubit]})
        return self

    def t_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.t_gate: [qubit]})
        return self

    def td_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.td_gate: [qubit]})
        return self

    def u_gate(self, theta, phi, lam, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.u_gate: [qubit],
                                constants.PARAMS: [theta, phi, lam]})
        return self

    def u1_gate(self, theta, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.u1_gate: [qubit],
                                constants.PARAMS: [theta]})
        return self

    def u2_gate(self, phi, lam, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.u2_gate: [qubit],
                                constants.PARAMS: [phi, lam]})
        return self

    def u3_gate(self, theta, phi, lam, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append(({OpType.u3_gate: [qubit],
                                 constants.PARAMS: [theta, phi, lam]}))
        return self

    def cy_gate(self, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.operations.append({OpType.cy_gate: [[control_qubit], [target_qubit]]})
        return self

    def i_gate(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.i_gate: [qubit]})
        return self

    def rccx_gate(self, control_qubit1, control_qubit2, target_qubit):
        self.check_qubit_boundary(control_qubit1)
        self.check_qubit_boundary(control_qubit2)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.rccx_gate: [[control_qubit1], [control_qubit2], [target_qubit]]})
        return self

    def rc3x_gate(self, control_qubit1, control_qubit2, control_qubit3, target_qubit):
        self.check_qubit_boundary(control_qubit1)
        self.check_qubit_boundary(control_qubit2)
        self.check_qubit_boundary(control_qubit3)
        self.check_qubit_boundary(target_qubit)
        self.operations.append(
            {OpType.rc3x_gate: [[control_qubit1], [control_qubit2], [control_qubit3], [target_qubit]]})
        return self

    def rxx_gate(self, theta, qubit1, qubit2):
        self.check_qubit_boundary(qubit1)
        self.check_qubit_boundary(qubit2)
        self.operations.append({OpType.rxx_gate: [[qubit1], [qubit2]], constants.PARAMS: [theta]})
        return self

    def rx_gate(self, theta, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.rx_gate: [qubit], constants.PARAMS: [theta]})
        return self

    def r_gate(self, theta, phi, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.r_gate: [qubit], constants.PARAMS: [theta, phi]})
        return self

    def p_gate(self, theta, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.p_gate: [qubit], constants.PARAMS: [theta]})
        return self

    def c3x_gate(self, control_qubit1, control_qubit2, control_qubit3, target_qubit):
        self.check_qubit_boundary(control_qubit1)
        self.check_qubit_boundary(control_qubit2)
        self.check_qubit_boundary(control_qubit3)
        self.check_qubit_boundary(target_qubit)
        self.operations.append(
            {OpType.c3x_gate: [[control_qubit1], [control_qubit2], [control_qubit3], [target_qubit]]})
        return self

    def c3sx_gate(self, control_qubit1, control_qubit2, control_qubit3, target_qubit):
        self.check_qubit_boundary(control_qubit1)
        self.check_qubit_boundary(control_qubit2)
        self.check_qubit_boundary(control_qubit3)
        self.check_qubit_boundary(target_qubit)
        self.operations.append(
            {OpType.c3sx_gate: [[control_qubit1], [control_qubit2], [control_qubit3], [target_qubit]]})
        return self

    def c4x_gate(self, control_qubit1, control_qubit2, control_qubit3, control_qubit4, target_qubit):
        self.check_qubit_boundary(control_qubit1)
        self.check_qubit_boundary(control_qubit2)
        self.check_qubit_boundary(control_qubit3)
        self.check_qubit_boundary(control_qubit4)
        self.check_qubit_boundary(target_qubit)
        self.operations.append(
            {OpType.c4x_gate: [[control_qubit1], [control_qubit2], [control_qubit3], [control_qubit4], [target_qubit]]})
        return self

    def dcx_gate(self, control_qubit1, control_qubit2):
        self.check_qubit_boundary(control_qubit1)
        self.check_qubit_boundary(control_qubit2)
        self.operations.append({OpType.dcx_gate: [[control_qubit1], [control_qubit2]]})
        return self

    def ch_gate(self, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.ch_gate: [[control_qubit], [target_qubit]]})
        return self

    def csx_gate(self, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.csx_gate: [[control_qubit], [target_qubit]]})
        return self

    def cswap_gate(self, control_qubit, target_qubit1, target_qubit2):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit1)
        self.check_qubit_boundary(target_qubit2)
        self.operations.append({OpType.cswap_gate: [[control_qubit], [target_qubit1], [target_qubit2]]})
        return self

    def cphase_gate(self, theta, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.cphase_gate: [[control_qubit], [target_qubit]],
                                constants.PARAMS: [theta]})
        return self

    def crx_gate(self, theta, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.crx_gate: [[control_qubit], [target_qubit]],
                                constants.PARAMS: [theta]})
        return self

    def cry_gate(self, theta, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.cry_gate: [[control_qubit], [target_qubit]],
                                constants.PARAMS: [theta]})
        return self

    def crz_gate(self, theta, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.crz_gate: [[control_qubit], [target_qubit]],
                                constants.PARAMS: [theta]})
        return self

    def cu_gate(self, theta, phi, lam, gamma, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.cu_gate: [[control_qubit], [target_qubit]],
                                constants.PARAMS: [theta, phi, lam, gamma]})
        return self

    def cu1_gate(self, theta, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.cu1_gate: [[control_qubit], [target_qubit]],
                                constants.PARAMS: [theta]})
        return self

    def cu3_gate(self, theta, phi, lam, control_qubit, target_qubit):
        self.check_qubit_boundary(control_qubit)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.cu3_gate: [[control_qubit], [target_qubit]],
                                constants.PARAMS: [theta, phi, lam]})
        return self

    def mcx_gate(self, control_qubits, target_qubit, ancilla_qubits=[], mode='nonancilla'):
        self.check_qubit_boundary(target_qubit)
        for qubit in control_qubits:
            self.check_qubit_boundary(qubit)
        self.operations.append({OpType.mcx_gate: control_qubits[:] + [target_qubit] + ancilla_qubits[:],
                                constants.PARAMS: [len(control_qubits)]})
        return self

    def mcxgc_gate(self, control_qubits, target_qubit):
        self.check_qubit_boundary(target_qubit)
        for qubit in control_qubits:
            self.check_qubit_boundary(qubit)
        self.operations.append(
            {OpType.mcxgc_gate: control_qubits[:] + [target_qubit], constants.PARAMS: [len(control_qubits)]})
        return self

    def mcxvchain_gate(self, control_qubits, target_qubit, dirty_ancilla):
        self.check_qubit_boundary(target_qubit)
        for qubit in control_qubits:
            self.check_qubit_boundary(qubit)
        self.operations.append({OpType.mcxvchain_gate: control_qubits[:] + [target_qubit],
                                constants.PARAMS: [len(control_qubits), dirty_ancilla]})
        return self

    def mcxrec_gate(self, control_qubits, target_qubit):
        self.check_qubit_boundary(target_qubit)
        for qubit in control_qubits:
            self.check_qubit_boundary(qubit)
        self.operations.append(
            {OpType.mcxrec_gate: control_qubits[:] + [target_qubit], constants.PARAMS: [len(control_qubits)]})
        return self

    def mcp_gate(self, lam, control_qubits, target_qubit):
        self.check_qubit_boundary(target_qubit)
        for qubit in control_qubits:
            self.check_qubit_boundary(qubit)
        self.operations.append(
            {OpType.mcp_gate: control_qubits[:] + [target_qubit], constants.PARAMS: [lam, len(control_qubits)]})
        return self

    def mct_gate(self, control_qubits, target_qubit, ancilla_qubits=None, mode='noancilla'):
        # self.check_qubit_boundary(control_qubit1)
        self.check_qubit_boundary(target_qubit)
        self.operations.append({OpType.mct_gate: [control_qubits, [target_qubit], ancilla_qubits, mode]})
        return self

    def measure(self, qubit):
        self.check_qubit_boundary(qubit)
        self.operations.append({OpType.measure: [qubit]})

    def measure_all(self):
        self.operations.append({OpType.measure_all: OpType.measure_all})

    def get_operations(self):
        return self.operations

    def check_qubit_boundary(self, qubit):
        if qubit > (self.qubits - 1):
            raise CircuitError(ErrorMessages.QUBIT_OUT_OF_BOUND)

    def draw_circuit(self, provider=providers.DEFAULT_PROVIDER):
        self.check_and_convert(provider)

        if self.provider == providers.IBM_PROVIDER:
            print(self.converted_q_circuit.draw())
        elif self.provider == providers.GOOGLE_PROVIDER:
            print(self.converted_q_circuit)
        elif self.provider == providers.MICROSOFT_PROVIDER:
            pass
        elif self.provider == providers.AMAZON_PROVIDER:
            print(self.converted_q_circuit)

    def convert_circuit(self):
        converted_q_circuit = None
        if self.provider == providers.IBM_PROVIDER:
            converted_q_circuit = convert.to_qiskit(self, self.qubits)
        elif self.provider == providers.GOOGLE_PROVIDER:
            converted_q_circuit = convert.to_cirq(self, self.qubits)
        elif self.provider == providers.IONQ_PROVIDER:
            converted_q_circuit = convert.to_cirq(self, self.qubits)
        elif self.provider == providers.MICROSOFT_PROVIDER:
            converted_q_circuit = convert.to_q_sharp(self, self.qubits)
        elif self.provider == providers.AMAZON_PROVIDER:
            converted_q_circuit = convert.to_braket(self, self.qubits)
        return converted_q_circuit

    def execute(self, provider=providers.DEFAULT_PROVIDER,
                simulator_name=constants.DEFAULT_SIMULATOR,
                repetitions=constants.DEFAULT_REPETITIONS,
                api=None, device=None,
                default_target='simulator', bucket=None,
                poll_timeout_seconds=100, poll_interval_seconds=10,
                directory=None):
        self.check_and_convert(provider)
        if self.provider == providers.IBM_PROVIDER:
            return execute_circuit.on_qiskit(self.converted_q_circuit,
                                             simulator_name, repetitions,
                                             api, device)
        elif self.provider == providers.GOOGLE_PROVIDER:
            return execute_circuit.on_cirq(self.converted_q_circuit,
                                           simulator_name, repetitions, api, self.get_operations())
        elif self.provider == providers.AMAZON_PROVIDER:
            return execute_circuit.on_braket(self.converted_q_circuit,
                                             simulator_name, repetitions, device, bucket, directory,
                                             poll_timeout_seconds=poll_timeout_seconds,
                                             poll_interval_seconds=poll_interval_seconds)
        elif self.provider == providers.IONQ_PROVIDER:
            if api is None:
                raise APIDetailsNotFoundError(ErrorMessages.IONQ_API_DETAILS_NOT_PROVIDED)
            return execute_circuit.on_ionq(self.converted_q_circuit,
                                           default_target, repetitions, api, self.get_operations())

    def check_and_convert(self, provider):
        if self.converted_q_circuit is None or self.provider != provider:
            self.provider = provider
            converted_q_circuit = self.convert_circuit()
            self.converted_q_circuit = converted_q_circuit

    def superposition(self, qubit):
        self.h_gate(qubit)

    def entangle(self, qubit1, qubit2):
        self.superposition(qubit1)
        self.cx_gate(qubit1, qubit2)

    def phase_kickback(self, qubit):
        self.x_gate(qubit)
        self.h_gate(qubit)

    @staticmethod
    def plot_bar(counts, color=constants.DEFAULT_COLOR, title=None, xlabel=None,
                 ylabel='Probabilities'):
        x_coord = []
        y_coord = []
        for key in counts:
            x_coord.append(key)
            y_coord.append(float("{:.3f}".format(counts[key] / sum(counts.values()))))
        fig, ax = plt.subplots()
        ax.bar(x_coord, y_coord, color=color, width=.10)
        ax.set_title(title)
        plt_gca = plt.gca()
        plt.bar_label(plt_gca.containers[0])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def compare_results(self, providers_list=None, repetitions=constants.DEFAULT_REPETITIONS):
        output_dict = {}
        if providers_list is None:
            providers_list = [providers.GOOGLE_PROVIDER, providers.IBM_PROVIDER, providers.AMAZON_PROVIDER]
            for provider in range(len(providers_list)):
                results = self.execute(provider=providers_list[provider], repetitions=repetitions)
                output_dict[providers_list[provider]] = results
        else:
            for provider_json in providers_list:
                provider = provider_json['provider']
                api = None if 'api' not in provider_json else provider_json['api']
                device = None if 'device' not in provider_json else provider_json['device']
                bucket = None if 'bucket' not in provider_json else provider_json['bucket']
                directory = None if 'directory' not in provider_json else provider_json['directory']
                simulator = constants.DEFAULT_SIMULATOR if 'simulator' not in provider_json \
                    else provider_json['simulator']
                repetitions = constants.DEFAULT_REPETITIONS if 'repetitions' not in provider_json \
                    else provider_json['repetitions']
                poll_timeout_seconds = 100 if 'poll_timeout_seconds' not in provider_json \
                    else provider_json['poll_timeout_seconds']
                poll_interval_seconds = 10 if 'poll_interval_seconds' not in provider_json \
                    else provider_json['poll_interval_seconds']

                results = self.execute(provider=provider, simulator_name=simulator,
                                       repetitions=repetitions, api=api, device=device,
                                       bucket=bucket, poll_timeout_seconds=poll_timeout_seconds,
                                       poll_interval_seconds=poll_interval_seconds, directory=directory)
                output_dict[provider_json['provider']] = results

        return output_dict

