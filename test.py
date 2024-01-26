import pandas as pd
import matplotlib.pyplot as plt

# pd.set_option('display.max_colwidth', None)

df = pd.read_excel('dataset.xlsx')

def search_bird(bird_name):
    bird_name = bird_name.lower()
    
    result = df[df['Name'].str.lower().str.contains(bird_name)]
    
    if not result.empty:
        return result
    else:
        print(f"No matching result found for '{bird_name}'.")

name_of_bird = input("Enter the name of bird: ")

res = search_bird(name_of_bird)

if not res.empty:
    print(res[['Name', 'Conservation status', 'Description']])

    color_mapping = {
        'Least Concern': 'green',
        'Near Threatened': 'yellow',
        'Vulnerable': 'orange',
        'Endangered': 'red',
    }

    bars = plt.bar(res['Name'], height=1, color=res['Conservation status'].map(color_mapping))

    legend_labels = {value: key for key, value in color_mapping.items()}
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in color_mapping.values()]
    plt.legend(legend_handles, legend_labels.values(), title='Conservation Status', loc='upper left')

    plt.xlabel('Bird Name')
    plt.ylabel('Conservation Status')
    plt.title('Conservation Status of Birds')
    plt.show()
