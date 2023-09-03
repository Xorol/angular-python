import tokenize as tkz
from pprint import pprint
from sys import argv
from os import system

# Get the output and input filepaths
# from command line args
output_file = "out.apy"
match len(argv):
  case 2:
    file_to_compile = argv[1]
  case 3:
    file_to_compile = argv[1]
    output_file = argv[2]
  case _:
    quit("Usage: python3 angular.py <input_path> [output_path]")

def annotation_valid(tok) -> bool:
  return tok.type == 1 or tok.string in ["<", ">", ">>", "...", ",", "[", "]", "|", ":"]

# Extract source code
with open(file_to_compile, "r") as src_file:
  src: str = src_file.read()

with open(file_to_compile, "r") as src_file:
  tokens = list(tkz.generate_tokens(src_file.readline))

current_annotation = []
annotations = []
annotation_idxs: list[list[int]] = []
generics = []
generic = False
depth = 0

# Find annotations
for i, tok in enumerate(tokens):
  if i in [0, len(tokens)]: # no annotations at the start nor end
    continue

  if tok.string == "def":
    generic = True
  elif tok.string == ")" and not current_annotation:
    generic = False
    
  # If the current token is not valid in an annotation
  # then obviously we're not parsing one
  if not annotation_valid(tok):
    current_annotation = []
    depth = 0
    continue

  # If we're not currently parsing an annotation
  # and the current token is not `<', starting one
  # Then continue
  if not current_annotation:
    if tok.string != "<":
      continue
    # we've found an annotation
    generics.append(int(generic))
    generic = False
    annotation_idxs.append([i])
  
  # We're parsing an annotation
  # and the current token is valid, so go ahead
  # and add it
  current_annotation.append(tok)

  # change the depth according to the brackets (`>>' is here bc it's tokenized as rshift)
  match tok.string:
    case "<":
      depth += 1
    case ">":
      depth -= 1
    case ">>":
      depth -= 2

  # If we're still parsing, continue
  if depth != 0:
    continue

  # we're done parsing the annotation, add it to the list of annotations
  annotations.append(current_annotation)
  current_annotation = []
  annotation_idxs[-1].append(i+1)

del current_annotation, depth
#pprint(annotations)

new_annotations = []

# Replace all instances of `<' and `>' with 
# `[' and `]', respectively within all the 
# annotations
for annotation in annotations:
  new_annotations.append([])

  for tok in annotation:
    match tok.string:
      case ">":
        # Replace > with ]
        new_tok = [tkz.TokenInfo(tkz.RSQB, "]", tok.start, tok.end, tok.line)]
      case "<":
        # Replace < with [
        new_tok = [tkz.TokenInfo(tkz.LSQB, "[", tok.start, tok.end, tok.line)]
      case ">>":
        # Replace >> with ]]
        new_tok = [
          tkz.TokenInfo(tkz.RSQB, "]", tok.start, (tok.end[0], tok.end[1]-1), tok.line),
          tkz.TokenInfo(tkz.RSQB, "]", (tok.start[0], tok.start[1]+1), tok.end, tok.line),
        ]
      case _:
        new_tok = [tok]
        
    new_annotations[-1].extend(new_tok)

#pprint(new_annotations)

# replace the old annotations with the new
for i, annotation in enumerate(new_annotations):
  annotation_idx = annotation_idxs[i]
  is_generic = generics[i]
  tokens[annotation_idx[0]+is_generic:annotation_idx[1]+is_generic] = annotation

#print("".join([t.string for t in tokens]))
compiled = tkz.untokenize(tokens)

# write the compiled code to the output file
# if the output file wasn't supplied, run it
with open(output_file, "w") as output:
  output.write(compiled)

if len(argv) != 3:
  system(f"python3 {output_file}")
  system(f"rm {output_file}")
