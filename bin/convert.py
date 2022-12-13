import sys
import argparse
import pandas as pd
import json
import requests

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input_libraryname')
    parser.add_argument('output_summary')
    parser.add_argument('output_filename')

    args = parser.parse_args()

    gnps_url = "https://gnps-external.ucsd.edu/gnpslibrary/{}.json".format(args.input_libraryname)

    all_spectra_list = requests.get(gnps_url).json()
    summary_list = []

    output_mgf = open(args.output_filename, "w")

    scan = 1
    for spectrum in all_spectra_list:
        spectrum["new_scan"] = scan
        
        output_mgf.write("BEGIN IONS\n")
        output_mgf.write("PEPMASS={}\n".format(spectrum["Precursor_MZ"]))
        output_mgf.write("CHARGE={}\n".format(spectrum["Charge"]))
        output_mgf.write("MSLEVEL={}\n".format(2))
        output_mgf.write("TITLE=Scan Number: ={}\n".format(scan))
        output_mgf.write("SCANS={}\n".format(scan))

        peaks = json.loads(spectrum["peaks_json"])
        for peak in peaks:
            output_mgf.write("{} {}\n".format(peak[0], peak[1]))

        output_mgf.write("END IONS\n")

        summary_dict = {}
        summary_dict["spectrum_id"] = spectrum["spectrum_id"]
        summary_dict["scan"] = scan
        summary_dict["Precursor_MZ"] = spectrum["Precursor_MZ"]
        summary_dict["Charge"] = spectrum["Charge"]
        summary_dict["Smiles"] = spectrum["Smiles"]
        summary_dict["INCHI"] = spectrum["INCHI"]
        summary_dict["InChIKey_smiles"] = spectrum["InChIKey_smiles"]
        summary_dict["InChIKey_inchi"] = spectrum["InChIKey_inchi"]

        summary_list.append(summary_dict)
        
        scan += 1

    output_mgf.close()

    summary_df = pd.DataFrame(summary_list)
    summary_df.to_csv(args.output_summary, index=False)

if __name__ == '__main__':
    main()