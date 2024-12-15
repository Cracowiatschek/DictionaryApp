from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # Generowanie pustej tabeli
    n = 10  # Liczba wierszy
    data = [{"row": i + 1, "editable": f"Editable {i + 1}", "dropdown": ""} for i in range(n)]
    options = ["Option 1", "Option 2", "Option 3"]  # Opcje dla dropdown
    return render_template('index.html', data=data, options=options)

@app.route('/update', methods=['POST'])
def update():
    updated_data = request.json  # Otrzymane dane z tabeli
    print("Updated Data:", updated_data)  # Możesz zapisać te dane w bazie
    return jsonify({"status": "success", "data": updated_data})

@app.route('/login', methods=['POST'])
def log():
    updated_data = request.get_json()  # Otrzymane dane z tabeli
    print("Updated Data:", updated_data)  # Możesz zapisać te dane w bazie
    return jsonify({"status": "success", "data": updated_data})

if __name__ == '__main__':
    app.run(debug=True)
