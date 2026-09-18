from flask import Flask, request, jsonify
import subprocess
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logging.info(f"Received Alert: {data}")
    alerts = data.get('alerts', [])
    
    for alert in alerts:
        if alert.get('labels', {}).get('alertname') == 'AppHighFailureRate':
            logging.info("Triggering Ansible Playbook for Remediation...")
            
            res = subprocess.run(
                ["ansible-playbook", "kubernetes/heal.yml"],
                capture_output=True,
                text=True
            )
            
            logging.info(f"Ansible Output:\n{res.stdout}")
            return jsonify({"status": "healed via ansible", "output": res.stdout}), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
