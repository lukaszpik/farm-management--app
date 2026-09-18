import stat

from fastapi.testclient import TestClient
from main import app
from backend.app.database.database import connection

client = TestClient(app)

## FARM
def test_get_all_farms():
    response = client.get("/farm/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_get_farm():
    response = client.get("/farm/1")
    assert response.status_code == 200

    data = response.json()
    assert data["farm_id"] == 1
    assert "name" in data
    assert "fid_numer" in data
    assert "position" in data
    assert "info" in data


def test_get_farm_not_found():
    response = client.get("/farm/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Farm with ID 999999 not found."


def test_create_farm():
    farm = {
        "name": "TEST FARM11",
        "fid_numer": 991,
        "position": "TEST",
        "info": "Farm created for testing"
    }

    response = client.post("/farm/", json=farm)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "TEST FARM11"
    assert data["fid_numer"] == 991
    assert data["position"] == "TEST"
    assert data["info"] == "Farm created for testing"

    response = client.get("/farm/")
    assert response.status_code == 200

    farms = response.json()
    farm_id = next(farm["farm_id"] for farm in farms if farm["fid_numer"] == 991)
    response = client.delete(f"/farm/{farm_id}")
    assert response.status_code == 200
    



def test_update_farm():
    farm = {
        "name": "TEST FARM PATCH",
        "fid_numer": 999998,
        "position": "TEST",
        "info": "Farm for PATCH test"
    }

    response = client.post("/farm/", json=farm)
    assert response.status_code == 200

    response = client.get("/farm/")
    assert response.status_code == 200
    farms = response.json()

    farm_id = next(
        farm["farm_id"]
        for farm in farms
        if farm["fid_numer"] == 999998)

    update_data = {
        "name": "UPDATED FARM",
        "position": "UPDATED POSITION"
    }

    response = client.patch(f"/farm/{farm_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == (f"Farm with ID {farm_id} updated successfully.")

    response = client.get(f"/farm/{farm_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "UPDATED FARM"
    assert data["position"] == "UPDATED POSITION"

    response = client.delete(f"/farm/{farm_id}")
    assert response.status_code == 200


def test_delete_farm():
    farm = {
        "name": "TEST FARM DELETE",
        "fid_numer": 999997,
        "position": "TEST",
        "info": "Farm for DELETE test"
    }

    response = client.post("/farm/", json=farm)
    assert response.status_code == 200

    response = client.get("/farm/")
    assert response.status_code == 200

    farms = response.json()
    farm_id = next(
        farm["farm_id"]
        for farm in farms
        if farm["fid_numer"] == 999997
    )

    response = client.delete(f"/farm/{farm_id}")
    assert response.status_code == 200
    assert response.json()["message"] == (f"Farm with ID {farm_id} deleted successfully.")

    response = client.get(f"/farm/{farm_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == (f"Farm with ID {farm_id} not found.")

## ANIMALS
def test_get_all_animals():
    response = client.get("/farms/1/animals/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

def test_get_animal():
    response = client.get("/farms/1/animals/1")
    assert response.status_code == 200
    data = response.json()

def test_get_animal_not_found():
    response = client.get("/farms/1/animals/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Animal with ID 999999 not found."

def test_add_animal():
    animal = {
        "farm_id": 1,
        "aid_numer": "TEST-007",
        "kind": "bydlo",
        "race": "HF",
        "utility": "mleczny",
        "sex": "samica",
        "date_of_birth": "2024-01-15"
    }

    response = client.post("/farms/1/animals/", json=animal) 
    assert response.status_code == 200

    data = response.json()
    assert data["aid_numer"] == animal["aid_numer"]
    assert data["kind"] == animal["kind"]
    assert data["race"] == animal["race"]
    assert data["utility"] == animal["utility"]
    assert data["sex"] == animal["sex"]
    assert data["date_of_birth"] == animal["date_of_birth"]

    animal_id = data["id"]
    delete_response = client.delete(f"/farms/1/animals/{animal_id}")
    assert delete_response.status_code == 200

def test_update_animal():
    animal = {
        "farm_id": 1,
        "aid_numer": "TEST-PATCH",
        "kind": "bydlo",
        "race": "HF",
        "utility": "mleczny",
        "sex": "samica",
        "date_of_birth": "2024-01-15"
    }

    response = client.post("/farms/1/animals/", json=animal)
    assert response.status_code == 200
    animal_id = response.json()["id"]

    update_data = {
        "utility": "miesny",
        "race": "Limousine"
    }

    response = client.patch(f"/farms/1/animals/{animal_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == (f"Animal with ID {animal_id} updated successfully.")

    response = client.get(f"/farms/1/animals/{animal_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["utility"] == "miesny"
    assert data["race"] == "Limousine"

    response = client.delete(f"/farms/1/animals/{animal_id}")
    assert response.status_code == 200


def test_delete_animal():
    animal = {
        "farm_id": 1,
        "aid_numer": "TEST-DELETE",
        "kind": "bydlo",
        "race": "HF",
        "utility": "mleczny",
        "sex": "samica",
        "date_of_birth": "2024-01-15"
    }

    response = client.post("/farms/1/animals/", json=animal)
    assert response.status_code == 200
    animal_id = response.json()["id"]

    response = client.delete(f"/farms/1/animals/{animal_id}")
    assert response.status_code == 200
    assert response.json()["message"] == (f"Animal with ID {animal_id} deleted successfully.")

    response = client.get(f"/farms/1/animals/{animal_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == (f"Animal with ID {animal_id} not found.")

## CROPS

def test_get_all_crops():
    response = client.get("/farms/1/fields/1/crops/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        crop = data[0]

        assert "id" in crop
        assert "field_id" in crop
        assert "name" in crop
        assert "type" in crop
        assert "area" in crop
        assert "year" in crop


def test_get_crop():
    response = client.get("/farms/1/fields/1/crops/pszenica")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

def test_get_crop_not_found():
    response = client.get("/farms/1/fields/1/crops/NIEISTNIEJACY_CROP")
    assert response.status_code == 404
    assert response.json()["detail"] == ("Crop with name NIEISTNIEJACY_CROP not found." )

def test_add_crop():
    crop = {
        "name": "TEST-CROP3",
        "type": "zboze",
        "area": 12.5,
        "year": 2026
    }

    response = client.post("/farms/1/fields/1/crops/", json=crop)
    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "TEST-CROP3"
    assert data["type"] == "zboze"
    assert data["area"] == 12.5
    assert data["year"] == 2026

    response = client.get("/farms/1/fields/1/crops/")
    assert response.status_code == 200
    crops = response.json()

    crop_id = next(
        crop["id"]
        for crop in crops
        if crop["name"] == "TEST-CROP3"
    )

    delete_response = client.delete(f"/farms/1/fields/1/crops/{crop_id}")
    assert delete_response.status_code == 200

def test_update_crop():
    crop = {
        "name": "TEST-CROP-PATCH",
        "type": "zboze",
        "area": 10.0,
        "year": 2026
    }

    response = client.post("/farms/1/fields/1/crops/", json=crop)
    assert response.status_code == 200

    response = client.get("/farms/1/fields/1/crops/TEST-CROP-PATCH")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0

    crop_id = data[0]["id"]
    update_data = {
        "type": "oleiste",
        "area": 15.5
    }

    response = client.patch(f"/farms/1/fields/1/crops/{crop_id}", json=update_data)
    assert response.status_code == 200

    response = client.get("/farms/1/fields/1/crops/TEST-CROP-PATCH")
    assert response.status_code == 200

    data = response.json()
    crop = data[0]

    assert crop["type"] == "oleiste"
    assert crop["area"] == 15.5

    response = client.delete(f"/farms/1/fields/1/crops/{crop_id}")
    assert response.status_code == 200

def test_delete_crop(): 
    crop = { 
        "name": "TEST-CROP-DELETE",
        "type": "zboze", "area": 8.0,
        "year": 2026 } 

    response = client.post( "/farms/1/fields/1/crops/", json=crop ) 
    assert response.status_code == 200 

    response = client.get( "/farms/1/fields/1/crops/TEST-CROP-DELETE" ) 
    assert response.status_code == 200
    data = response.json() 
    assert len(data) > 0 

    crop_id = data[0]["id"] 
    response = client.delete( f"/farms/1/fields/1/crops/{crop_id}" ) 
    assert response.status_code == 200 
    assert response.json()["message"] == ( f"Crop with ID {crop_id} deleted successfully." ) 

    response = client.get( "/farms/1/fields/1/crops/TEST-CROP-DELETE" ) 
    assert response.status_code == 404 
    assert response.json()["detail"] == ( "Crop with name TEST-CROP-DELETE not found." )

 ## FIELDS 
def test_get_all_fields():
    response = client.get("/farms/1/fields/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        field = data[0]
        assert "field_id" in field
        assert "farm_id" in field
        assert "type" in field
        assert "position" in field
        assert "area" in field


def test_get_field():
    response = client.get("/farms/1/fields/1")
    assert response.status_code == 200
    data = response.json()

    assert data["field_id"] == 1
    assert data["farm_id"] == 1
    assert "type" in data
    assert "position" in data
    assert "area" in data

def test_add_field():
    field = {
        "farm_id": 1,
        "type": "grunty_orne",
        "position": "TEST",
        "area": 12.5
    }

    response = client.post("/farms/1/fields/", json=field)
    assert response.status_code == 200
    data = response.json()

    assert "field_id" in data
    assert data["farm_id"] == 1
    assert data["type"] == "grunty_orne"
    assert data["position"] == "TEST"
    assert data["area"] == 12.5

    field_id = data["field_id"]
    response = client.delete(f"/farms/1/fields/{field_id}")
    assert response.status_code == 200

def test_update_field():
    field = {
        "farm_id": 1,
        "type": "grunty_orne",
        "position": "TEST",
        "area": 12.5
    }

    response = client.post("/farms/1/fields/", json=field)
    assert response.status_code == 200
    field_id = response.json()["field_id"]

    update_data = {
        "type": "grunty_orne",
        "area": 25.5
    }

    response = client.patch(f"/farms/1/fields/{field_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == (f"Field with ID {field_id} from Farm 1 updated successfully.")

    response = client.get(f"/farms/1/fields/{field_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["field_id"] == field_id
    assert data["farm_id"] == 1
    assert data["type"] == "grunty_orne"
    assert data["area"] == 25.5

    response = client.delete(f"/farms/1/fields/{field_id}")
    assert response.status_code == 200


def test_delete_field():
    field = {
        "farm_id": 1,
        "type": "grunty_orne",
        "position": "TEST",
        "area": 10.0
    }

    response = client.post("/farms/1/fields/", json=field)
    assert response.status_code == 200

    field_id = response.json()["field_id"]
    response = client.delete(f"/farms/1/fields/{field_id}")

    assert response.status_code == 200
    assert response.json()["message"] == (f"Field with ID {field_id} from Farm 1 deleted successfully.")

## FIELDWORK

def test_get_all_fieldworks():
    response = client.get("/farms/1/fields/1/fieldworks/")
    assert response.status_code == 200
    data =  response.json()
    assert isinstance(data, list)
    
    if data:
        field = data[0]
        assert "field_id" in field
        assert "type_of_work" in field
        assert "method" in field
        assert "date" in field
        assert "cost" in field



def test_add_fieldwork():
    fieldwork_data = {
        "type_of_work": "talerzowanie",
        "method": "wlasna",
        "date": "2026-09-18",
        "cost": 250.50,
    }

    response = client.post("/farms/1/fields/1/fieldworks/", json=fieldwork_data)
    assert response.status_code == 200
    data = response.json()

    assert data["type_of_work"] == "talerzowanie"
    assert data["method"] == "wlasna"
    assert data["cost"] == 250.50
    assert data["date"] == "2026-09-18"

def test_get_fieldwork():
    response = client.get("/farms/1/fields/1/fieldworks/orka")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)



def test_update_fieldwork():
    fieldwork_data = {
        "type_of_work": "prasowanie",
        "method": "wlasna",
        "cost": 1500,
        "date": "2026-09-18"
    }

    add_response = client.post("/farms/1/fields/1/fieldworks/", json=fieldwork_data)
    assert add_response.status_code == 200

    fieldwork_id = add_response.json()["id"]
    update_data = {
        "cost": 300
    }

    response = client.patch(f"/farms/1/fields/1/fieldworks/{fieldwork_id}",json=update_data)
    assert response.status_code == 200


def test_delete_fieldwork():
    fieldwork_data = {
        "type_of_work": "orka",
        "method": "wlasna",
        "cost": 400,
        "date": "2026-09-18"
    }

    response = client.post("/farms/1/fields/1/fieldworks/", json=fieldwork_data)
    assert response.status_code == 200

    fieldwork_id = response.json()["id"]
    response = client.delete(f"/farms/1/fields/1/fieldworks/{fieldwork_id}")
    assert response.status_code == 200

## MACHINES

def test_get_all_machines():
    response = client.get("/farms/1/machines/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_get_machine():
    response = client.get("/farms/1/machines/ciągnik")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_add_machine():
    machine_data = {
        "type": "ciągnik",
        "name": "Testowy ciągnik",
        "model": "Test 500",
        "manufacture": 2020
    }

    response = client.post(
        "/farms/1/machines/",
        json=machine_data
    )
    assert response.status_code == 200

    data = response.json()
    assert data["type"] == "ciągnik"
    assert data["name"] == "Testowy ciągnik"
    assert data["model"] == "Test 500"
    assert data["manufacture"] == 2020


def test_update_machine():
    update_data = {
        "name": "Zaktualizowany ciągnik"
    }

    response = client.patch(
        "/farms/1/machines/1",
        json=update_data
    )
    assert response.status_code == 200

def test_update_nonexistent_machine():
    update_data = {
        "name": "Zaktualizowana maszyna"
    }
    response = client.patch(f"/farms/1/machines/999999", json=update_data)
    assert response.status_code == 200

def test_delete_machine():
    machine_data = {
        "type": "ciagnik",
        "name": "TEST Ursus",
        "model": "1014",
        "manufacture": 1992
    }

    response = client.post(f"/farms/1/machines", json=machine_data)
    assert response.status_code == 200
    machines = client.get("/farms/1/machines/").json()

    for machine in machines:
        if machine["name"] == "TEST Ursus":
            machine_id = machine["id"]
            break
    assert machine_id is not None

    response = client.delete(f"/farms/1/machines/{machine_id}")
    assert response.status_code == 200

## FINANCES

def test_add_financial_record():
    financial_data = {
        "type": "przychod",
        "category": "paliwo",
        "amount": 5000,
        "performer": "test",
        "date": "2026-09-18",
        "info": "test financial record"
    }

    response = client.post(f"/farms/1/finances/", json=financial_data)
    assert response.status_code == 200

    data = response.json()
    assert data["type"] == "przychod"
    assert data["category"] == "paliwo"
    assert data["amount"] == 5000
    assert data["performer"] == "test"
    assert data["date"] == "2026-09-18"
    assert data["info"] == "test financial record"

    response = client.get("/farms/1/finances/") 
    assert response.status_code == 200 
    records = response.json() 
 
    for record in records: 
        if ( record["category"] == "paliwo" and record["date"] == "2026-09-18" and record["info"] == "test financial record" ): 
            finance_id = record["id"] 
            break 
    assert finance_id is not None

    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM financial_records WHERE id = %s",
            (finance_id,)
        )
        connection.commit()


def test_update_financial_record():
    financial_data = {
        "type": "przychod",
        "category": "paliwo",
        "amount": 5000,
        "performer": "test",
        "date": "2026-09-18",
        "info": "test financial record"
    }

    response = client.post(f"/farms/1/finances/", json=financial_data)
    assert response.status_code == 200

    update_data = {
        "amount": 6000
    }

    data = client.get("/farms/1/finances/")
    assert data.status_code == 200
    records = data.json()

    for record in records: 
            if (record["category"] == "paliwo" and record["date"] == "2026-09-18" and record["info"] == "test financial record" ): 
                finance_id = record["id"] 
                break  
    assert finance_id is not None

    patch = client.patch(f"/farms/1/finances/", params={"id": finance_id}, json=update_data)
    assert patch.status_code == 200

    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM financial_records WHERE id = %s",(finance_id,))
        connection.commit()


def test_get_financial_summary():
    response = client.get(f"/farms/1/finances/summary",params={"date_from": "2026-01-01", "date_to": "2026-12-31"})
    assert response.status_code == 200

    data = response.json()
    assert "income" in data
    assert "costs" in data


def test_get_income_summary():
    response = client.get(f"/farms/1/finances/income", params={"date_from": "2026-01-01", "date_to": "2026-12-31"})
    assert response.status_code == 200

    data = response.json()
    assert "income" in data


def test_get_all_financial_records():
    response = client.get("/farms/1/finances/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)




