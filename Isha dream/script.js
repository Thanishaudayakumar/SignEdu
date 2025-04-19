<input type="text" id="searchQuery" placeholder="Search rhymes..." />
<button onclick="searchRhyme()">Search</button>

<script>
async function searchRhyme() {
    const query = document.getElementById("searchQuery").value;
    const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
    });
    const data = await response.json();
    if (data.error) {
        alert(data.error);
    } else {
        alert(`Result: ${data.rhyme}`);
    }
}
</script>
