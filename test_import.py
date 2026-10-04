try:
    import app.services.llm
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
