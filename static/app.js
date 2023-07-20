const form = document.querySelector("form");
const ul = document.querySelector("ul");
const flavor = document.querySelector("#flavor");
const size = document.querySelector("#size");
const rating = document.querySelector("#rating");
const image = document.querySelector("#image");

document.addEventListener("DOMContentLoaded", async () => {
    let { data } = await axios.get("/api/cupcakes");
    for (el of data.cupcakes) {
        let li = document.createElement("li");
        for (key of Object.keys(el)) {
            let item = document.createElement("div");
            item.innerHTML = `<span>${key}: ${el[key]}</span>`;
            li.append(item);
        }
        ul.append(li)
    }
});

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const { data } = await axios.post('/api/cupcakes', form, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
});