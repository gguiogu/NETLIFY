text = open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8").read()

# Find the digital market section start and end
start_marker = "        <!-- Digital Services Section -->"
end_marker = "        <!-- Market Section Ends Here -->"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker) + len(end_marker)

if start_idx == -1 or end_idx == -1:
    print("MARKERS NOT FOUND")
    print("start:", start_idx, "end:", end_idx)
else:
    print(f"Section found: lines {start_idx} to {end_idx}")
    print("Preview start:", text[start_idx:start_idx+100])
    print("Preview end:", text[end_idx-100:end_idx])
