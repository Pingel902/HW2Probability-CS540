import sys
import math

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    '''
    This function reads text from filename and counts characters A-Z (case-insensitive)
    Returns: dictionary with counts for each letter
    '''
    # Initialize dictionary with all uppercase letters set to 0
    X = {chr(i): 0 for i in range(ord('A'), ord('Z')+1)}
    
    try:
        with open(filename, encoding='utf-8') as f:
            text = f.read()
            
            # Convert text to uppercase for case-insensitive counting
            text = text.upper()
            
            # Count each letter
            for char in text:
                # Check if character is A-Z
                if 'A' <= char <= 'Z':
                    X[char] += 1
                    
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)
        
    return X

def log(num, probs):

    if num == 0 or probs == 0:
        return 0.0
    
    return num * math.log(probs)

def f_value(X, probs, prior):
    log_prob = 0.0

    for i, char in enumerate(range(ord('A'), ord('Z')+1)):
        counts = X[chr(char)]
        probability  = probs[i]
        log_prob += log(counts, probability)

    return math.log(prior) + log_prob

def main():
    # Checking Command Line Arguments
    if len(sys.argv) != 4:
        print("Usage: python3 hw2.py [letter file] [english prior] [spanish prior]")
        sys.exit(1)
        
    letter = sys.argv[1]  #First Command Line Argument

    eng = float(sys.argv[2])  #Second Command Line Argument

    span = float(sys.argv[3])  #Third Command Line Argument
    
    # Getting number of letters in the file
    X = shred(letter)
    
    # Get parameter vectors
    e, s = get_parameter_vectors()
    
    # Printing the character counts -> Q1
    print("Q1")
    for char in range(ord('A'), ord('Z')+1):
        print(f"{chr(char)} {X[chr(char)]}")
    
    # Calculating and printing X₁log(e₁) and X₁log(s₁) for Q2
    print("Q2")
    e_var = log(X['A'], e[0])
    s_var   = log(X['A'], s[0])
    print(f"{e_var:.4f}")
    print(f"{s_var:.4f}")
    
    # Calculating and printing F(English) and F(Spanish) for Q3
    print("Q3")
    fE = f_value(X, e, eng)
    fS = f_value(X, s, span)
    print(f"{fE:.4f}")
    print(f"{fS:.4f}")

    # Calculating and printing P(Y=English|X) for Q4
    print("Q4")
    dif = fS - fE
    
    if dif >= 100:
        probE = 0.0
    elif dif <= -100:
        probE = 1.0
    else:
        probE = 1.0 / (1.0 + math.exp(dif))
    
    print(f"{probE:.4f}")

if __name__ == "__main__":
    main()