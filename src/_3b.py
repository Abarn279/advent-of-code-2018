from file_importer import FileImporter

class Claim():
    def __init__(self, id, x, y, w, h):
        self.id = id
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.no_overlap = True

def get_claims(claim_strs):
    claims = []
    for claim_str in claim_strs:
        claim_str = claim_str.split(' ')
        claim = Claim(
            id = claim_str[0][1:],
            x = int(claim_str[2].split(',')[0]),
            y = int(claim_str[2].split(',')[1][:-1]),
            w = int(claim_str[3].split('x')[0]),
            h = int(claim_str[3].split('x')[1])
        )
        claims.append(claim)
    return claims

# Solution
claim_strs = FileImporter.get_input("/../input/3.txt").split("\n")

claims = get_claims(claim_strs)                                     # List of claims
grid = [['.' for i in range(1000)] for j in range(1000)]            # 1000x1000 grid

for claim in claims:
    for row in range(claim.y, claim.y + claim.height):
        for col in range(claim.x, claim.x + claim.width):
            if grid[row][col] == '.':                               # Never been hit before
                grid[row][col] = claim.id
            else:                        
                claims[int(grid[row][col]) - 1].no_overlap = False  # Mark the claim that had this space as being overlapped
                claim.no_overlap = False                            # Also mark the current claim as overlapped

for claim in claims:
    if claim.no_overlap:
        print(claim.id)
        break
