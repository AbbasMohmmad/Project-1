def crop_unaccess_sequences(input_filename, output_filename, access_txt):
    length = 0
    with open(access_txt, 'r') as f:
        for line in f:
            seq = line.strip()
            length = len(seq)
            break
        print(length)
    sequences = []

    # Read sequences from the input file, skipping header lines
    with open(input_filename, 'r') as f:
        for line in f:
            if not line.startswith('>'):
                sequences.append(line.strip())

    # Calculate the optimal length as the median length of sequences
    lengths = [len(seq) for seq in sequences]
    optimal_length = length

    # Crop sequences to the optimal length
    cropped_sequences = []
    for seq in sequences:
        if len(seq) >= optimal_length:
            start_index = (len(seq) - optimal_length) // 2
            end_index = start_index + optimal_length
            cropped_sequences.append(seq[start_index:end_index])

    # Write cropped sequences to the output file
    with open(output_filename, 'w') as f:
        for seq in cropped_sequences:
            f.write(seq + '\n')
    print("OP", length)

    return optimal_length
trim_unacc = input("Enter filename for trimmed unaccess file ")
input_filename = input("Enter unaccess txt file ")
acc_seq = input("Enter acc_seq text file ")
crop_unaccess_sequences(input_filename, trim_unacc, acc_seq) 
