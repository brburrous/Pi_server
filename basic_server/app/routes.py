from flask import render_template, request, jsonify
from app import app, move
ports = move.usb_id()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/drive', methods=['POST'])
def drive():
    try:
        ports = move.usb_id()
        json = request.json
        direction = json["direction"]
        drive = json["drive"] 
        cmd = "drive_" + direction
        if drive == 'TRUE':
            move.take_command(cmd, ports)
            return f'Successfully moved bot', 200
        else:
            move.finish(ports)
            return f'Successfully stopped bot', 200
    except Exception as e:
        return f"An Error Occured: {e}", 400

@app.route('/head', methods=['POST'])
def head():
    try:
        ports = move.usb_id()
        json=request.json
        direction = json["direction"]
        move = json["move"]
        cmd = "head_" + direction
        if move == 'TRUE':
            move.take_command(cmd, ports)
            return "Successfully moved bot's head", 200
        else:
            move.finish(ports)
            return "Successfully stoped bot", 400
    except Exception as e:
        return f"An Error Occured {e}", 400

@app.route('/dispense', methods=['POST'])
def dispense():
    try:
        ports = move.usb_id()
        json=request.json
        bin=json["bin"]
        cmd = "payload_" + bin
        move.take_command(cmd, ports)
        return "Successfully dispensed item", 200
    except Exception as e:
        return f"An Error Occured {e}", 400

@app.route('/face', methods=['POST']) 
def face():
    try:
        
        json = request.json
        emotion = json["emotion"]
        duration = json["duration"]
        cmd = "face_" + emotion
        if duration != "":
            cmd += " " + duration
        move.take_command(cmd, ports)
        return "Success", 200
    except Exception as e:
        return f"An Error Occured {e}", 400
