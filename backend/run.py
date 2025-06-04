from app import create_app

print(">>> RUN.PY is being executed")

app = create_app()
 
if __name__ == '__main__':
    print(">>> Running on PORT 5001")
    app.run(host='0.0.0.0', port=5001, debug=True)