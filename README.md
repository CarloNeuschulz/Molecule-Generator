# MolGen.pyp (Generated by Copilot, edidted by Carlo Neuschulz)

### This is my project for my three week internship at Maxon Computer Gmbh.
### It was very fun :D

## Description
MolGen.pyp is a Python script that generates molecular structures based on user-defined rules and parameters. It utilizes a combination of algorithms and data structures to create diverse and realistic molecules.

## Features
- Rule-based generation: Define rules for atom types, bond types, and molecular properties to guide the generation process.
- Customizable parameters: Adjust various parameters such as molecule size, bond length, and atom properties to control the output.
- Output formats: Export generated molecules in popular file formats such as PDB, SDF, or SMILES.
- Visualization: Visualize the generated molecules using integrated 3D rendering capabilities.

## Installation
1. Clone the repository or download the "MolGen.pyp" script.
2. Cinema 4D by Maxon needed. (dont forget to set the plugin directory to where you safed the "MolGen.pyp" file.) 
3. Install the required dependencies by running the following command:
    ```
    pip install -r requirements.txt
    ```
4. Point 2. is very important :D you can get a liscens on https://www.maxon.net/de/buy 
(ps. you can get a studen licens :D )
## Usage
1. Open a terminal  and navigate to the directory containing the "MolGen.pyp" script. 
2. Run the script using the following command:
    ```
    python MolGen.pyp
    ```
3. Follow the on-screen prompts to specify the generation rules and parameters.
4. Once the generation is complete, the generated molecules will be saved in the specified output format.

5. (Terminal? Open "Edit", go to "Prefrences", select "Plugins" redirect your directory to where the Plugin is located, open "Extensions" and click on "Molecule Generator Plugin")

## Examples
Here are a few examples of how to use the script:

- Use the dropdowns. For that you have to click on one of the options in the dropdown and press "Create Molecule" and it creats the Linear/Cyclic alkane.

- Or insert your own formular based on the scientificyl ground formular, for linear its CnHn*2+2 and for Cyclic its CnHn*2. 

- If you are still unsure how the Plugin works press the "Help?" button and read through the steps to figure out how to use the plugin.

(Copilot wrote that i have no idea why but im going to leave it there anyway :D )
- Generate a small molecule with default parameters:
  ```
  python MolGen.pyp --size small
  ```

- Generate a large molecule with custom rules:
  ```
  python MolGen.pyp --size large --rules rules.json
  ```

- Generate a molecule and save it in PDB format:
  ```
  python MolGen.pyp --format pdb
  ```

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is Copyright: MAXON Computer GmbH and Carlo Neuschulz 

## Contact
For any questions or inquiries, please contact [Carlo.Neuschulz@gmail.com]

##### Thanks to all at Maxon for taking me in as an intern, showing me everything and giving me the oppertunity to work with amazing people that helped me develop this script. <3
##### Special thanks to Jana Bröckling and Ilia Mazlov for looking after me. (it was one of the best easter holidays for me) :D