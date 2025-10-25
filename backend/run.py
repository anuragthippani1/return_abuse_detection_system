from app import create_app
import os

print(">>> RUN.PY is being executed")

app = create_app()
 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f">>> Running on PORT {port}")
    app.run(host='0.0.0.0', port=port, debug=False)