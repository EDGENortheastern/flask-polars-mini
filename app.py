from flask import Flask, render_template, request, redirect, url_for #Python web framework
import polars as pl # fast DataFrame library (like pandas)
import plotly.graph_objects as go # Plotly is for charts

app = Flask(__name__)

@app.get("/")
def home():
    return redirect(url_for("upload_form"))

@app.get("/health")
def health():
    return {"flask": "ok", "polars_version": pl.__version__}

@app.get("/upload")
def upload_form():
    return render_template("upload.html")

@app.post("/upload")
def upload_file():
    file = request.files["csvfile"]
    if not file or file.filename == "":
        return "No file selected", 400

    df = pl.read_csv(file)

    preview = df.head(5)
    preview_rows = preview.to_dicts()
    preview_cols = preview.columns

    # Pick first numeric column (if any) and make a chart
    numeric_cols = [c for c, dt in zip(df.columns, df.dtypes) if dt.is_numeric()]
    graph_html = None
    graph_title = None
    if numeric_cols:
        col = numeric_cols[0]
        values = df[col].to_list()
        fig = go.Figure(data=[go.Box(x=values)])
        fig.update_layout(title=f"Histogram of {col}", xaxis_title=col, yaxis_title="Count")
        graph_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
        graph_title = f"Histogram of {col}"

    return render_template(
        "summary.html",
        rows=df.height,
        columns=df.width,
        colnames=df.columns,
        preview_cols=preview_cols,
        preview_rows=preview_rows,
        graph_html=graph_html,
        graph_title=graph_title,
    )

if __name__ == "__main__":
    app.run(debug=True)
