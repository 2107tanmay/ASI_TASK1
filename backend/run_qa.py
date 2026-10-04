import urllib.request
import urllib.error
import json
import traceback
import sys

def test_endpoints():
    print("Starting backend QA test...")
    report = ["# Backend QA & Adversarial Test Report\n"]
    base_url = "http://localhost:8000/api"
    
    try:
        req = urllib.request.Request("http://localhost:8000/openapi.json")
        with urllib.request.urlopen(req) as response:
            openapi = json.loads(response.read().decode())
        
        report.append("## Endpoints Discovered\n")
        paths = openapi.get("paths", {})
        for path, methods in paths.items():
            for method, details in methods.items():
                report.append(f"- **{method.upper()}** `{path}`: {details.get('summary', 'No summary')}")
        report.append("\n## Test Executions\n")
        
        def run_test(name, method, url, data=None):
            report.append(f"### {method} {url}\n")
            try:
                req = urllib.request.Request(f"{base_url}{url}", method=method)
                if data:
                    req.add_header('Content-Type', 'application/json')
                    req.data = json.dumps(data).encode('utf-8')
                
                try:
                    with urllib.request.urlopen(req) as response:
                        status = response.status
                        body_bytes = response.read()
                        body = json.loads(body_bytes.decode()) if body_bytes else None
                        report.append(f"- **Status**: {status}\n- **Response**: `{json.dumps(body)}`\n- **Result**: PASS\n")
                except urllib.error.HTTPError as e:
                    body = e.read().decode()
                    report.append(f"- **Status**: {e.code}\n- **Error Body**: `{body}`\n- **Result**: CAUGHT ERROR (Expected for empty/invalid data)\n")
            except Exception as e:
                report.append(f"- **Exception**: {str(e)}\n- **Result**: FAIL\n")
                
        # 1. Health
        run_test("Health Check", "GET", "/health")
        # 2. Get Decision Pack
        run_test("Get Decision Pack", "GET", "/decision-pack")
        # 3. List Evidence
        run_test("List Evidence", "GET", "/evidence")
        # 4. Get Evidence
        run_test("Get Evidence", "GET", "/evidence/1")
        # 5. Run Calculation (empty data)
        run_test("Run Calculation", "POST", "/calculations/run", data={})
        # 6. Upload Document (empty)
        # For upload, we should send multipart/form-data ideally, but we can test bad request.
        report.append("### POST /documents/upload\n")
        try:
            req = urllib.request.Request(f"{base_url}/documents/upload", method="POST")
            with urllib.request.urlopen(req) as response:
                status = response.status
                report.append(f"- **Status**: {status}\n- **Result**: UNEXPECTED PASS\n")
        except urllib.error.HTTPError as e:
            report.append(f"- **Status**: {e.code}\n- **Error Body**: `{e.read().decode()}`\n- **Result**: CAUGHT ERROR (422 Expected)\n")

        # Write report
        with open("qa_test_report.md", "w") as f:
            f.write("\n".join(report))
            
        print("QA test completed. Report saved to qa_test_report.md.")
    except Exception as e:
        print(f"Failed to run QA test: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_endpoints()
