from fastapi import APIRouter
from ..repositories import repo_machines
from ..schemas import Machines, MachineUpdate, MachineAdd

machines = APIRouter(prefix="/farms/{farm_id}/machines")


@machines.get("/", response_model=list[Machines])
def get_all_machines(farm_id: int):
    return repo_machines.get_all_machines(farm_id)


@machines.get("/{type}", response_model=list[Machines])
def get_machine(farm_id: int, type: str):
    return repo_machines.get_machine(farm_id, type)


@machines.post("/", response_model=MachineAdd)
def add_machine(farm_id: int, machine: MachineAdd):
    return repo_machines.add_machine(farm_id, machine)


@machines.patch("/{id}")
def update_machine(farm_id: int, id: int, machine: MachineUpdate):
    return repo_machines.update_machine(farm_id, id, machine)


@machines.delete("/{id}")
def delete_machine(farm_id: int, id: int):
    return repo_machines.delete_machine(farm_id, id)