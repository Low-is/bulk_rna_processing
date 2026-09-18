# Reading bulk RNA-seq FASTQ files
import glob
import subprocess
import os
import csv
import re



# ---------------------------------------------------------
# Directories
# ---------------------------------------------------------
#fastq_directory_striatum = "D:/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/LJO1JHU504_striatum/fastq/"  # Window path
#fastq_directory_choroid_plexus = "D:/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/LJO1JHU505_choroid_plexus/fastq/" 

fastq_directory_striatum = "/mnt/d/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/LJO1JHU504_striatum/fastq/"
fastq_directory_choroid_plexus = "/mnt/d/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/LJO1JHU505_choroid_plexus/fastq/" 



#output_directory_striatum = "D:/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/LJO1JHU504_striatum/star_output/"
output_directory_striatum = "/mnt/d/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/LJO1JHU504_striatum/star_output/"

#output_directory_choroid_plexus = "D:/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/LJO1JHU505_choroid_plexus/star_output/"
output_directory_choroid_plexus = "/mnt/d/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/LJO1JHU505_choroid_plexus/star_output/"

#genome_directory = "D:/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/genomes/h38/STAR/" 
genome_directory = "/mnt/d/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/genomes/h38/STAR/"


# ---------------------------------------------------------
# Function to run STAR
# ---------------------------------------------------------
def run_star(fastq_directory, output_directory):

    os.makedirs(output_directory, exist_ok=True)

    # Find R1 FASTQ files
    r1_files = glob.glob(
        os.path.join(fastq_directory, "*_R1.trimmed.fastq.gz")
    )[:1]

    for r1 in r1_files:

        # Get corresponding R2 file
        r2 = r1.replace(
            "_R1.trimmed.fastq.gz",
            "_R2.trimmed.fastq.gz"
        )

        if not os.path.exists(r2):
            print("WARNING: R2 file not found for:")
            print(r1)
            continue

        # Extract sample name
        sample_name = os.path.basename(r1).replace(
            "_R1.trimmed.fastq.gz",
            ""
        )

        # Create output directory
        sample_output = os.path.join(
            output_directory,
            sample_name + "_output"
        )

        os.makedirs(sample_output, exist_ok=True)

        print("\nCurrently mapping:", sample_name)

        # STAR command
        command = [
            "STAR",
            "--runThreadN", "64",
            "--genomeDir", genome_directory,

            "--readFilesIn",
            r1,
            r2,

            "--readFilesCommand", "zcat",

            "--outFilterType", "BySJout",
            "--outFilterMismatchNoverLmax", "0.04",
            "--outFilterMismatchNmax", "999",
            "--alignSJDBoverhangMin", "1",
            "--alignSJoverhangMin", "8",
            "--outFilterMultimapNmax", "20",
            "--alignIntronMin", "20",
            "--alignIntronMax", "1000000",
            "--alignMatesGapMax", "1000000",

            "--outSAMtype",
            "BAM",
            "SortedByCoordinate",

            "--quantMode",
            "GeneCounts",

            "--outFileNamePrefix",
            sample_output + "/"
        ]

        subprocess.run(command, check=True)

        print("Finished:", sample_name)


# ---------------------------------------------------------
# Run STAR
# ---------------------------------------------------------
run_star(
  fastq_directory_striatum,
  output_directory_striatum
)

#run_star(
  #fastq_directory_choroid_plexus,
  #output_directory_choroid_plexus
#)

# ---------------------------------------------------------
# Create count matrix
# ---------------------------------------------------------

def create_count_matrix(output_directory, output_prefix):

    #desired_column = 1 # unstranded
    desired_column = 2 # sense counts
    #desired_column = 3 # antisense counts

    sample_dict = {}
    sample_names = []

    for folder in os.listdir(output_directory):

        if folder.endswith("_output"):

            sample_name = folder.removesuffix("_output")

            count_file = os.path.join(
                output_directory,
                folder,
                "ReadsPerGene.out.tab"
            )

            if not os.path.exists(count_file):
                print("WARNING: count file not found:")
                print(count_file)
                continue

            sample_names.append(sample_name)

            gene_dict = {}

            with open(count_file) as tabfile:

                print(
                    "Column",
                    desired_column,
                    "of",
                    sample_name,
                    "stored"
                )

                reader = csv.reader(
                    tabfile,
                    delimiter="\t"
                )

                for row in reader:
                    gene_dict[row[0]] = row[desired_column]

            sample_dict[sample_name] = gene_dict

    # Sort samples for reproducibility
    sample_names.sort()

    # Sort genes
    sorted_genes = sorted(
        sample_dict[sample_names[0]].keys()
    )

    # Output files
    raw_counts_file = output_prefix + "_raw_counts.csv"
    qc_file = output_prefix + "_qc.csv"

    with open(raw_counts_file, "w", newline="") as counts_file, \
         open(qc_file, "w", newline="") as qc_file:

        counts_writer = csv.writer(counts_file)
        qc_writer = csv.writer(qc_file)

        counts_writer.writerow(
            ["gene"] + sample_names
        )

        qc_writer.writerow(
            ["qc_metric"] + sample_names
        )

        for gene in sorted_genes:

            output = [gene]

            for sample in sample_names:
                output.append(
                    sample_dict[sample][gene]
                )

            if gene.startswith("N_"):
                qc_writer.writerow(output)

            else:
                counts_writer.writerow(output)

    print("\nCreated:")
    print(raw_counts_file)
    print(qc_file)


# ---------------------------------------------------------
# Create count matrices
# ---------------------------------------------------------

create_count_matrix(
    output_directory_striatum,
    "striatum"
)

#create_count_matrix(
    #output_directory_choroid_plexus,
    #"choroid_plexus"
#)
