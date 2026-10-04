echo "Extracting..."
Expand-Archive neo4j.zip -DestinationPath neo4j_dir -Force
echo "Setting password..."
$neo4jBin = (Get-ChildItem -Path neo4j_dir -Filter neo4j-admin.bat -Recurse).FullName
& $neo4jBin dbms set-initial-password password
echo "Starting Neo4j..."
$neo4jStart = (Get-ChildItem -Path neo4j_dir -Filter neo4j.bat -Recurse).FullName
Start-Process -FilePath $neo4jStart -ArgumentList "start" -NoNewWindow
echo "Wait for startup..."
Start-Sleep -Seconds 20
