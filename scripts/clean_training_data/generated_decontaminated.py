import argparse
import glob
import json
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="dedup dataset based on ngram.")
    parser.add_argument(
        "-indir",
        "--input_directory",
        default=os.path.expanduser("~/datasets/latent/sft_2.8m_dedup"),
    )
    parser.add_argument(
        "-overlap",
        "--overlap_file",
        default="decontaminate_latent/matched/final_overlap.json",
    )
    parser.add_argument(
        "-outfile",
        "--output_jsonl",
        default="decontaminate_latent/decontaminated.jsonl",
    )
    args = parser.parse_args()

    files = list(sorted(glob.glob(os.path.join(args.input_directory, "*.jsonl"))))

    # Load overlap data
    with open(args.overlap_file, "r") as overlap_file:
        overlap = json.load(overlap_file)

    # Extract doc_ids from overlap
    bad = set(record["doc_id"] for record in overlap)

    # Initialize global offset
    pile_global_offset = 0

    # Process the files and write output
    with open(args.output_jsonl, "w") as outfile:
        for file_i, file in enumerate(files):
            with open(file, "r") as f:
                for document in f:
                    document = document.strip()
                    if document:
                        # Check if the document's global offset is not in the bad set
                        if pile_global_offset not in bad:
                            outfile.write(document + "\n")
                        else:
                            print(f"skip {pile_global_offset}")
                        pile_global_offset += 1
