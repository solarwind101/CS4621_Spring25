# Author: Suraj Sharma, CS-4621, Spring 2025, Assignment 3
# Email: suraj.sharma_ugt2023@ashoka.edu.in

# Implementation of Arithmetic Encoding and Decoding based on incremental encoding and decoding algorithm

import random

def arithmetic_encode(message, cdf, symbols, probs):
    L, U = 0.0, 1.0
    bitstream = []
    #e3_count = 0

    for s in message:
        R = U - L
        lower_cdf = (cdf[s] - probs[s])
        upper_cdf = (cdf[s])

        U = L + R * upper_cdf
        L = L + R * lower_cdf

        while True:
            if U < 0.5:
                L, U = 2 * L, 2 * U
                bitstream.append("0")

                # Uncomment the following block if E3 scaling is applied.
                # if e3_count > 0:
                #    bitstream.append("1" * e3_count)
                #    e3_count = 0
            

            elif L >= 0.5:
                bitstream.append("1")
                L, U = 2 * (L - 0.5), 2 * (U - 0.5)

                # Uncomment the following block if E3 scaling is applied.
                # if e3_count > 0:
                #    bitstream.append("0" * e3_count)
                #    e3_count = 0

            # Uncomment the following block for E3 scaling
            # elif (L >= 0.25 and U < 0.75):
            #     L, U = 2 * (L - 0.25), 2 * (U - 0.25)
            #     e3_count += 1
            else:
                break

    bitstream = "".join(bitstream)
    return bitstream

def get_tag(bits):
    tag = 0.0
    power = 0.5
    for i in bits:
        if i == '1':
            tag += power
        power *= 0.5
    return tag  

def arithmetic_decode(bitstream, cdf, probs, win_size=5, message_len=0):

    # The window size is usually chosen based on the shortest tag interval. When the encoder encodes the message, there will be a case where the difference between U and L is minimal.
    # During such interval, the number of bits generated will be maximum. To successfully decode the first element unambiguously, the window size must be at least as large as 
    # the number of bits generated during that interval. This ensures that even if the first symbol corresponds to the shortest tag interval, we have enough bits to decode it precisely.
    # Here, we are choosing a sufficiently large window size (e.g., 15 to 20 bits), assuming it will not fail. However, the ideal approach is to determine the shortest tag interval 
    # from the encoder and use the corresponding number of bits as the window size.

    L = 0.0
    U = 1
    tag_bit = bitstream[0: win_size]
    tag = get_tag(tag_bit)
    bit_index = 0
    decoded_message = []
    
    while len(decoded_message) < message_len:
        R = U - L
        
        for s, cdf_s in cdf.items():
            lower_limit = cdf_s - probs[s]
            upper_limit = cdf_s
            if L + R * lower_limit <= tag < L + R * upper_limit:
                decoded_message.append(s)
                U = L + R * upper_limit
                L = L + R * lower_limit
                break
    
        while True:
            if U < 0.5:
                L, U = 2 * L, 2 * U
                bit_index += 1
                tag_bit = bitstream[bit_index: bit_index + win_size]
                tag = get_tag(tag_bit)

                # Uncomment the following block if E3 scaling is applied.
                # if e3_count > 0:
                    #  bit_index += e3_count
                    #  e3_count = 0
                    #  tag_bit = bitstream[bit_index: bit_index + win_size]
                    #  tag = get_tag(tag_bit)

            elif L >= 0.5:
                L, U = 2 * (L - 0.5), 2 * (U - 0.5)
                bit_index += 1
                tag_bit = bitstream[bit_index: bit_index + win_size]
                tag = get_tag(tag_bit)

                # Uncomment the following block if E3 scaling is applied.
                # if e3_count > 0:
                    #  bit_index += e3_count
                    #  e3_count = 0
                    #  tag_bit = bitstream[bit_index: bit_index + win_size]
                    #  tag = get_tag(tag_bit)

            # Uncomment the following block for E3 scaling
            # elif L >= 0.25 and U < 0.75:
            #     L, U = 2 * (L - 0.25), 2 * (U - 0.25)
            #     e3_count += 1
            else:
                break
        
    return decoded_message

import random
symbols = [1, 2, 3, 4, 5]
probs = {1: 1/2, 2: 1/4, 3: 1/8, 4: 1/16, 5: 1/16}
cdf = {}
cumulative_sum = 0

for s in symbols:
    cumulative_sum += probs[s]
    cdf[s] = cumulative_sum

n = 1000
messages = [random.choices(symbols, weights=probs.values(), k=1)[0] for _ in range(n)]

len_m = len(messages)
encoded_message = arithmetic_encode(messages, cdf, symbols, probs)
print('Message is:', messages)
print("Encoded message is:", encoded_message)

decoded_message = arithmetic_decode(encoded_message, cdf, probs, win_size=15, message_len=len_m)
print("Decoded message is:", decoded_message)

# check if the decoded message matches the original message
mismatch_indices = [i for i, (m1, m2) in enumerate(zip(messages, decoded_message)) if m1 != m2]

if mismatch_indices:
    print(f"Mismatches found at indices: {mismatch_indices}")
    print("Decoding failed.")
else:
    print("All elements match.")
    print("Decoding successful.")
