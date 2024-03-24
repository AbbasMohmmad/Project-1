import numpy as np

optimal = 0
def edit_sequences(input_file, output_file):
    # Read the sequences from the input file and calculate their lengths
    seq_list = []
    with open(input_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                continue  # Skip header lines
            seq_list.append(line.strip())

    # Determine the optimal length (median length)
    seq_lengths = np.array([len(seq) for seq in seq_list])
    optimal_length = int(np.median(seq_lengths))
    optimal = optimal_length

    # Crop sequences to the optimal length
    cropped_seqs = []
    for seq in seq_list:
        if len(seq) >= optimal_length:
            start = (len(seq) - optimal_length) // 2
            end = (len(seq) + optimal_length) // 2
            cropped_seq = seq[start:end]
            cropped_seqs.append(cropped_seq)

    with open(output_file, 'w') as f:
        f.writelines(seq + '\n' for seq in cropped_seqs)


def generate_unaccessible_bed(input_bed_filename, output_bed_filename):
    with open(input_bed_filename, 'r') as bed_file:
        lines = bed_file.readlines()

    list_data = []
    for line in lines:
        if not line.startswith('#'):  # Skip comment lines if any
            chromosome, start, end = line.strip().split('\t')[:3]
            list_data.append((chromosome, int(start), int(end)))
    unaccessible_list_data = []
    last = 1
    chromosome = None
    for i, (ch, start, end) in enumerate(list_data):
        if i == len(list_data) - 1:
            continue  # skipping the last iteration
        if chromosome is None:
            chromosome = ch
            last = end + 1
            continue
        elif last != start and chromosome == ch:
            if last - 1 != start and last - 1 < start:
                unaccessible_list_data.append((ch, last, start - 1))
                last = end + 1
                chromosome = ch
        else:
            chromosome = ch
            last = end + 1

    with open(output_bed_filename, 'w') as output_file:
        output_file.writelines('\t'.join(map(str, interval)) + '\n' for interval in unaccessible_list_data)

    return output_bed_filename

# Example usage:

access_input = input("Enter accessible input file ")
access_output = input("Enter accessible output file ")
edit_sequences(access_input, access_output)

input_bed_file = input("Enter input bed file ")
output_bed_file = input("Enter output bed file ")
unacc_bed = generate_unaccessible_bed(input_bed_file, output_bed_file)

