import unittest

import hashlib
from ogs6py.ogs import OGS

class TestiOGS(unittest.TestCase):

    def test_buildfromscratch(self):
        model = OGS(PROJECT_FILE="tunnel_ogs6py.prj", MKL=True, OMP_NUM_THREADS=4)
        model.mesh.addMesh(filename="tunnel.vtu")
        model.mesh.addMesh(filename="tunnel_left.vtu")
        model.mesh.addMesh(filename="tunnel_right.vtu")
        model.mesh.addMesh(filename="tunnel_bottom.vtu")
        model.mesh.addMesh(filename="tunnel_top.vtu")
        model.mesh.addMesh(filename="tunnel_inner.vtu")
        model.processes.setProcess(
            name="THERMO_RICHARDS_MECHANICS",
            type="THERMO_RICHARDS_MECHANICS",
            integration_order="3",
            specific_body_force="0 0",
            initial_stress="Initial_stress")
        model.processes.setConstitutiveRelation(type="LinearElasticIsotropic",
                                                youngs_modulus="E",
                                                poissons_ratio="nu")
        model.processes.addProcessVariable(process_variable="displacement",
                                        process_variable_name="displacement")
        model.processes.addProcessVariable(process_variable="pressure",
                                        process_variable_name="pressure")
        model.processes.addProcessVariable(process_variable="temperature",
                                        process_variable_name="temperature")
        model.processes.addProcessVariable(secondary_variable="sigma",
                                        output_name="sigma")
        model.processes.addProcessVariable(secondary_variable="epsilon",
                                        output_name="epsilon")
        model.processes.addProcessVariable(secondary_variable="velocity",
                                        output_name="velocity")
        model.processes.addProcessVariable(secondary_variable="saturation",
                                        output_name="saturation")

        model.media.addProperty(medium_id="0",
                                phase_type="AqueousLiquid",
                                name="specific_heat_capacity",
                                type="Constant",
                                value="4280.0")
        model.media.addProperty(medium_id="0",
                                phase_type="AqueousLiquid",
                                name="thermal_conductivity",
                                type="Constant",
                                value="0.6")
        model.media.addProperty(medium_id="0",
                                phase_type="AqueousLiquid",
                                name="density",
                                type="Linear",
                                reference_value="999.1",
                                variable_name="phase_pressure",
                                reference_condition="1e5",
                                slope="4.5999999999999996e-10")
        model.media.addProperty(medium_id="0",
                                phase_type="AqueousLiquid",
                                name="thermal_expansivity",
                                type="Constant",
                                value="3.98e-4")
        model.media.addProperty(medium_id="0",
                                phase_type="AqueousLiquid",
                                name="viscosity",
                                type="Constant",
                                value="1.e-3")
        model.media.addProperty(medium_id="0",
                                name="permeability",
                                type="Constant",
                                value="1e-17")
        model.media.addProperty(medium_id="0",
                                name="porosity",
                                type="Constant",
                                value="0.15")
        model.media.addProperty(medium_id="0",
                                phase_type="Solid",
                                name="density",
                                type="Constant",
                                value="2300")
        model.media.addProperty(medium_id="0",
                                phase_type="Solid",
                                name="thermal_conductivity",
                                type="Constant",
                                value="1.9")
        model.media.addProperty(medium_id="0",
                                phase_type="Solid",
                                name="specific_heat_capacity",
                                type="Constant",
                                value="800")
        model.media.addProperty(medium_id="0",
                                name="biot_coefficient",
                                type="Constant",
                                value="0.6")
        model.media.addProperty(medium_id="0",
                                phase_type="Solid",
                                name="thermal_expansivity",
                                type="Constant",
                                value="1.7e-5")
        model.media.addProperty(medium_id="0",
                                name="thermal_conductivity",
                                type="EffectiveThermalConductivityPorosityMixing")
        model.media.addProperty(medium_id="0",
                                name="saturation",
                                type="Constant",
                                value="1")
        model.media.addProperty(medium_id="0",
                                name="relative_permeability",
                                type="Constant",
                                value="1")
        model.media.addProperty(medium_id="0",
                                name="bishops_effective_stress",
                                type="BishopsPowerLaw",
                                exponent="1")
        model.timeloop.addProcess(process="THERMO_RICHARDS_MECHANICS",
                                nonlinear_solver_name="nonlinear_solver",
                                convergence_type="PerComponentDeltaX",
                                norm_type="NORM2",
                                abstols="1e-4 1e-4 1e-10 1e-10",
                                time_discretization="BackwardEuler")
        model.timeloop.setStepping(process="THERMO_RICHARDS_MECHANICS",
                                type="IterationNumberBasedTimeStepping",
                                t_initial=0,
                                t_end=8,
                                initial_dt=0.1,
                                minimum_dt=1e-7,
                                maximum_dt=0.1,
                                number_iterations=[1, 4, 10, 20],
                                multiplier=[1.2, 1.0, 0.9, 0.8])
        model.timeloop.addOutput(
            type="VTK",
            prefix="tunnel",
            repeat="10000",
            each_steps="1",
            variables=["displacement", "pressure", "temperature",
                    "sigma", "epsilon", "velocity", "saturation"],
            fixed_output_times=[1, 2, 3],
            suffix="_ts_{:timestep}_t_{:time}")
        model.parameters.addParameter(name="Initial_stress", type="Function",
                                    mesh="tunnel", expression=["-5e6", "-5e6", "-5e6", "0"])
        model.parameters.addParameter(name="E", type="Constant", value="2e9")
        model.parameters.addParameter(name="nu", type="Constant", value="0.3")
        model.parameters.addParameter(name="T0", type="Constant", value="273.15")
        model.parameters.addParameter(name="displacement0",
                                    type="Constant",
                                    values="0 0")

        model.parameters.addParameter(name="pressure_ic", type="Constant", value="1e6")
        model.parameters.addParameter(name="dirichlet0", type="Constant", value="0")
        model.parameters.addParameter(name="temperature_ic",
                                    type="Constant",
                                    value="293.15")
        model.parameters.addParameter(name="pressure_bc",
                                    type="CurveScaled",
                                    curve="excavation_curve",
                                    parameter="pressure_ic")
        model.parameters.addParameter(name="PressureLoad",
                                    type="CurveScaled",
                                    curve="excavation_curve",
                                    parameter="PressureLoadValue")
        model.parameters.addParameter(
            name="PressureLoadValue", type="Constant", value="-5.6e6")
        model.parameters.addParameter(name="heat_bv",
                                    type="Constant",
                                    value="25")
        model.curves.addCurve(name="excavation_curve", coords=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
                            values=[1.0, 1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.0])
        model.processvars.setIC(process_variable_name="temperature",
                                components="1",
                                order="1",
                                initial_condition="temperature_ic")
        model.processvars.addBC(process_variable_name="temperature",
                                mesh="tunnel_right",
                                type="Dirichlet",
                                component="0",
                                parameter="temperature_ic")
        model.processvars.addBC(process_variable_name="temperature",
                                mesh="tunnel_left",
                                type="Dirichlet",
                                component="0",
                                parameter="temperature_ic")
        model.processvars.addBC(process_variable_name="temperature",
                                mesh="tunnel_bottom",
                                type="Dirichlet",
                                component="0",
                                parameter="temperature_ic")
        model.processvars.addBC(process_variable_name="temperature",
                                mesh="tunnel_top",
                                type="Dirichlet",
                                component="0",
                                parameter="temperature_ic")

        model.processvars.setIC(process_variable_name="displacement",
                                components="2",
                                order="1",
                                initial_condition="displacement0")
        model.processvars.addBC(process_variable_name="displacement",
                                mesh="tunnel_right",
                                type="Dirichlet",
                                component="0",
                                parameter="dirichlet0")
        model.processvars.addBC(process_variable_name="displacement",
                                mesh="tunnel_left",
                                type="Dirichlet",
                                component="0",
                                parameter="dirichlet0")
        model.processvars.addBC(process_variable_name="displacement",
                                mesh="tunnel_top",
                                type="Dirichlet",
                                component="1",
                                parameter="dirichlet0")
        model.processvars.addBC(process_variable_name="displacement",
                                mesh="tunnel_bottom",
                                type="Dirichlet",
                                component="1",
                                parameter="dirichlet0")
        model.processvars.addBC(process_variable_name="displacement",
                                mesh="tunnel_inner",
                                type="NormalTraction",
                                parameter="PressureLoad")
        model.processvars.setIC(process_variable_name="pressure",
                                components="1",
                                order="1",
                                initial_condition="pressure_ic")
        model.processvars.addBC(process_variable_name="pressure",
                                mesh="tunnel_right",
                                type="Dirichlet",
                                component="0",
                                parameter="pressure_ic")
        model.processvars.addBC(process_variable_name="pressure",
                                mesh="tunnel_left",
                                type="Dirichlet",
                                component="0",
                                parameter="pressure_ic")
        model.processvars.addBC(process_variable_name="pressure",
                                mesh="tunnel_top",
                                type="Dirichlet",
                                component="0",
                                parameter="pressure_ic")
        model.processvars.addBC(process_variable_name="pressure",
                                mesh="tunnel_bottom",
                                type="Dirichlet",
                                component="0",
                                parameter="pressure_ic")
        model.processvars.addBC(process_variable_name="pressure",
                                mesh="tunnel_inner",
                                type="Dirichlet",
                                component="0",
                                parameter="pressure_bc")

        model.nonlinsolvers.addNonlinSolver(name="nonlinear_solver",
                                            type="Newton",
                                            max_iter="50",
                                            linear_solver="general_linear_solver")
        model.linsolvers.addLinSolver(name="general_linear_solver",
                                    kind="eigen",
                                    solver_type="PardisoLU")
        model.writeInput()
        with open("tunnel_ogs6py.prj", "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        self.assertEqual(file_hash.hexdigest(), '502dcb5b68d0ee2b5beb0ea735e8803e')


if __name__ == '__main__':
    unittest.main()
