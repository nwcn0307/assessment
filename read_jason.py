import json

# Opening JSON file
f = open('strings.json')

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json list
for i in data['strings']:
    print(i)


try:
    # Execute a SELECT statement
    cur.execute("SELECT * FROM dbdemo")

    # Fetch all the rows from the cursor
    rows = cur.fetchall()

    # Convert rows to a list of dictionaries
    records = []
    for row in rows:
        record = {}
        for i, column in enumerate(cur.description):
            record[column.name] = row[i]
        records.append(record)

    # Write records to a JSON file
    with open('output.json', 'w') as f:
        json.dump(records, f, indent=4)


# Closing file
f.close()