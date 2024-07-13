import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('data.csv')

# Combine 'Year' and 'Month' for X-axis
df['YearMonth'] = df['Year'].astype(str) + df['Month'].astype(str)

# Get unique 'Pathogen' values
pathogens = df['Pathogen'].unique()
print("Pathogens:")
for i, pathogen in enumerate(pathogens):
    print(f"{i+1}. {pathogen}")

# User selects a pathogen
pathogen_choice = int(input("Select a pathogen by number: "))
selected_pathogen = pathogens[pathogen_choice-1]

# Get unique 'Serotype/Species/Subgroup' values for the selected pathogen
serotypes = df[df['Pathogen'] == selected_pathogen]['Serotype/Species/Subgroup'].unique()
print("\nSerotypes:")
for i, serotype in enumerate(serotypes):
    print(f"{i+1}. {serotype}")

# User selects up to 4 serotypes
serotype_choices = list(map(int, input("Select up to 4 serotypes by number (separated by space): ").split()))
selected_serotypes = [serotypes[i-1] for i in serotype_choices]

# User selects Y-axis values
print("\n1. Number of isolates\n2. Past two years average and % Change")
y_choice = int(input("Select one by number: "))

# Set line styles and widths
styles = ['-', '-', ':', ':', '--', '--', '-.', '-.']
widths = [1, 2, 1, 2, 1, 2, 1, 2]

# Plot the data
plt.figure(figsize=(10, 6))
i = 0
for serotype in selected_serotypes:
    data = df[(df['Pathogen'] == selected_pathogen) & (df['Serotype/Species/Subgroup'] == serotype)]
    data = data.sort_values('YearMonth')
    if y_choice == 1:
        plt.plot(data['YearMonth'], data['Number of isolates'], label=serotype, linestyle=styles[i], linewidth=widths[i], color='black')
        plt.ylabel('Number of isolates')
        i += 1  # Increment the index after each line is plotted
    else:
        plt.plot(data['YearMonth'], data['Past two years average'], label=serotype+' avg', linestyle=styles[i], linewidth=widths[i], color='black')
        i += 1  # Increment the index after each line is plotted
        if i < 8:  # Ensure we don't exceed 8 lines
            plt.plot(data['YearMonth'], data['% Change'], label=serotype+' change', linestyle=styles[i], linewidth=widths[i], color='black')
            i += 1  # Increment the index after each line is plotted
        plt.ylabel('Percent')

plt.xlabel('YearMonth')
plt.title('Graph for ' + selected_pathogen)
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)

# Save the figure and data
filename = selected_pathogen + '_' + '_'.join(selected_serotypes)
filename = filename.replace('/', '-')  # replace '/' with '-'
plt.savefig(filename + '.png',dpi=300)
df.to_csv(filename + '.csv', index=False)

plt.show()

