from .errorHandler import handleError


@handleError("Failed to load SQL queries", internal_error=1)
def loadQueries(file_path="queries.sql"):
    queries = {}
    current_name = None
    current_sql = []

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("--"):
                if current_name and current_sql:
                    queries[current_name] = "\n".join(current_sql).strip()
                    current_sql = []
                current_name = line[2:].strip()
            elif line:
                current_sql.append(line)
        if current_name and current_sql:
            queries[current_name] = "\n".join(current_sql).strip()

    return queries
