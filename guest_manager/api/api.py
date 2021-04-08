import frappe
import json

def validate_booking(data, action='add'):
    try:
        if not frappe.db.exists({'doctype': 'Booking Resource', 'resource_name': data.get('resource')}):
            return {
                "status": "failed",
                "code": 404,
                "message": "Resource does not exist",
            }
        resource = frappe.db.get_all('Booking Resource', filters={'resource_name': data.get('resource')},
            fields=['name', 'max_capacity', 'concurrency'])
        overlap = []
        if action == 'add':
            overlap = frappe.db.get_all('Bookings', 
                filters={'resource': data['resource'], 'start_time': ['<=', data['start_time']], 'end_time': ['>', data['start_time']]}, 
                fields=['no_of_persons'])
            print(overlap)
            if not bool(overlap):
                overlap = frappe.db.get_all('Bookings',
                    filters={'resource': data['resource'], 'start_time': ['<', data['end_time']], 'end_time': ['>=', data['end_time']]}, 
                    fields=['no_of_persons'])
        elif action == 'update':
            if data.get('start_time') or data.get('end_time'):
                if data.get('end_time'):
                    overlap = frappe.db.get_all('Bookings', 
                        filters={'resource': data['resource'], 'name': ['!=', data['name']], 'start_time': ['<', data['end_time']], 'end_time': ['>', data['end_time']]},
                        fields=['no_of_persons'])
                if not bool(overlap) and data.get('start_time'):
                    overlap = frappe.db.get_all('Bookings', 
                        filters={'resource': data['resource'], 'name': ['!=', data['name']], 'start_time': ['<', data['start_time']], 'end_time': ['>', data['start_time']]},
                        fields=['no_of_persons'])
        print(overlap)
        if bool(overlap):
            if not resource[0].concurrency:
                return {
                    "status": "failed",
                    "code": 400,
                    "message": "Your time schedule for this resource may have an overlap. Please adjust your schedule",
                }
            existing_persons = 0
            for x in overlap:
                existing_persons = existing_persons + x.no_of_persons
            if action == 'add': 
                if resource[0].max_capacity <= existing_persons + data['no_of_persons']:
                    return {
                        "status": "failed",
                        "code": 400,
                        "message": "Maximum resource capacity exceeded",
                    }
            if action == 'update':
                if data.get('no_of_persons'):
                    if resource[0].max_capacity <= existing_persons + data['no_of_persons']:
                        return {
                            "status": "failed",
                            "code": 400,
                            "message": "Maximum resource capacity exceeded",
                        }
        if action == 'add': 
            if resource[0].max_capacity <= data.get('no_of_persons'):
                return {
                    "status": "failed",
                    "code": 400,
                    "message": "Maximum resource capacity exceeded",
                }
        if action == 'update':
            if data.get('no_of_persons'):
                if resource[0].max_capacity <= data.get('no_of_persons'):
                    return {
                        "status": "failed",
                        "code": 400,
                        "message": "Maximum resource capacity exceeded",
                    }
        return {
            "status": "success",
        }
    except:
        return {
            "status": "failed",
            "code": 400,
            'message': "Something went wrong",
        }

@frappe.whitelist(allow_guest=True)
def get_todos():
    # doc = frappe.get_doc('Todo')
    doc = frappe.db.get_all('ToDo', fields=["description", "status", "creation"])
    return {
        "ok": True,
        "statusCode": 200,
        "data": doc,
    }

@frappe.whitelist(allow_guest=True)
def get_bookings():
    #try:
    data = json.loads(frappe.request.data)
    if data.get('resource') and not data.get('start_time'):
        doc = frappe.db.get_all('Bookings', filters={'resource': data['resource'], 'start_time': ['>=', frappe.utils.nowdate()]},
            fields=['resource', 'start_time', 'end_time', 'capacity'],
            order_by = 'end_time desc')
        return {
            "status": "success",
            "code": 200,
            'message': "Bookings retrieved successfully",
            'data': doc,
        }
    elif data.get('start_time') and not data.get('resource'):
        doc = frappe.db.get_all('Bookings', filters={'start_time': ['>=', data['start_time']]},
            fields=['resource', 'start_time', 'end_time', 'capacity'],
            order_by = 'end_time desc')
        return {
            "status": "success",
            "code": 200,
            'message': "Bookings retrieved successfully",
            'data': doc,
        }
    elif data.get('start_time') and data.get('resource'):
        doc = frappe.db.get_all('Bookings', filters={'start_time': ['>=', data['start_time']], 'resource': data['resource']},
            fields=['resource', 'start_time', 'end_time', 'capacity'],
            order_by = 'end_time desc')
        return {
            "status": "success",
            "code": 200,
            'message': "Bookings retrieved successfully",
            'data': doc,
        }
    else:
        doc = frappe.db.get_all('Bookings', filters={'start_time': ['>=', frappe.utils.nowdate()]},
            fields=['resource', 'start_time', 'end_time', 'capacity'],
            order_by = 'end_time desc')
        return {
            "status": "success",
            "code": 200,
            'message': "Bookings retrieved successfully",
            'data': doc,
        }
    #except:
    #    return {
    #            "status": "failed",
    #            "code": 400,
    #            'message': "Something went wrong",
    #        }

@frappe.whitelist(allow_guest=True)
def add_booking():
    try:
        data = json.loads(frappe.request.data)
        resource = frappe.db.get_all('Booking Resource', filters={'resource_name': data['resource']},
                fields=['name', 'max_capacity'])
        result = validate_booking(data)
        if result["status"] == "failed":
            return result
        doc = frappe.new_doc('Bookings')
        doc.resource = data['resource']
        doc.start_time = data['start_time']
        doc.end_time = data['end_time']
        doc.no_of_persons = data['no_of_persons']
        doc.capacity = resource[0].max_capacity
        doc.insert()
        print(doc)
        return {
            "status": "success",
            "code": 200,
            'message': "Your reservation has been booked successfully",
            'data': doc,
        }
    except:
        return {
            "status": "failed",
            "code": 400,
            'message': "Something went wrong 1",
        }

@frappe.whitelist(allow_guest=True)
def remove_booking():
    try:
        data = json.loads(frappe.request.data)
        if frappe.db.exists('Bookings', data['name']):
            frappe.delete_doc('Bookings', data['name'])
            return {
                "status": "success",
                "code": 204,
                "message": "Reservation deleted successfully",
            }
        return {
                "status": "failed",
                "code": 404,
                "message": "Reservation not found",
            }
    except:
        return {
            "status": "failed",
            "code": 400,
            'message': "Something went wrong",
        }

@frappe.whitelist(allow_guest=True)
def update_booking():
    try:
        data = json.loads(frappe.request.data)
        resource = frappe.db.get_all('Booking Resource', filters={'resource_name': data['resource']},
                fields=['name', 'max_capacity'])
        result = validate_booking(data, action='update')
        if result["status"] == "failed":
            return result
        doc = frappe.get_doc('Bookings', data['name'])
        if data.get('start_time'):
            doc.start_time = data['start_time']
        if data.get('end_time'):
            doc.end_time = data['end_time']
        if data.get('no_of_persons'):
            doc.no_of_persons = data['no_of_persons']
        if data.get('resource'):
            doc.resource = data['resource']
            doc.capacity = resource[0].max_capacity
        doc.save()
        return {
                    "status": "success",
                    "code": 201,
                    "message": "Booking updated successfully",
                    "data": doc,
                }
    except:
        return {
            "status": "failed",
            "code": 400,
            'message': "Something went wrong",
        }
        
