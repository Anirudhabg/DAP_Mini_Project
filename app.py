from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import seaborn as sns

app = Flask(__name__)

df = pd.read_excel('featherGuard.xlsx')

def search_bird(bird_name):
    bird_name = bird_name.lower()
    if(len(bird_name)==0):
        result = pd.DataFrame()
        return result
    result = df[df['Name'].str.lower().str.contains(bird_name)]
    print(result)
    return result

def plot_bird_conservation(data):
    color_mapping = {
        'Least Concern': 'green',
        'Vulnerable': 'yellow',
        'Near Threatened': 'orange',
        'Endangered': 'red',
    }

    status_counts = data['Conservation status'].value_counts()

    plt.figure(figsize=(6, 6))
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=[color_mapping.get(status, 'gray') for status in status_counts.index])
    plt.title('Conservation Status of Birds')

    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plt.close()

    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    return img_base64

def plot_migration_pattern(data):
    migration_counts = data['Migration Pattern'].value_counts()
    
    plt.figure(figsize=(8, 6))
    migration_counts.plot(kind='bar', color='skyblue')
    plt.title('Migration Pattern Distribution')
    plt.xlabel('Migration Pattern')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plt.close()

    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    return img_base64

def plot_family(data):
    plt.figure(figsize=(10,6))
    sns.countplot(x="Family",data=data)
    plt.title("Distribution of birds on basis of family")
    plt.xlabel("Family")
    plt.ylabel("Count")

    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plt.close()

    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    return img_base64
    
def plot_geo_curv(data):
    plt.figure(figsize=(10,6))
    sns.countplot(x="Family",data=data)
    plt.title("Distribution of birds on basis of family")
    plt.xlabel("Family")
    plt.ylabel("Count")

    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plt.close()

    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    return img_base64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def result():
    name_of_bird = request.form['bird_name']
    res = search_bird(name_of_bird)

    if not res.empty:
        img_base64_conserv = plot_bird_conservation(res)
        img_base64_migr = plot_migration_pattern(res)
        img_base64_fam = plot_family(res)

        columns_to_exclude = ['ID']
        bird_data_html = res.drop(columns=columns_to_exclude).to_html(index=False)

        return render_template('index.html', bird_data=bird_data_html, img_base64_conserv=img_base64_conserv, img_base64_migr=img_base64_migr, img_base64_fam=img_base64_fam)
    else:
        return render_template('index.html', message=f"No matching result found for '{name_of_bird}'.")

if __name__ == '__main__':
    app.run(debug=True)
