// Mobile device check from Otree snippets

function isMobile() {
    const toMatch = [
        /Android/i,
        /iPhone/i,
        /iPad/i,
    ];

    return toMatch.some((toMatchItem) => {
        return navigator.userAgent.match(toMatchItem);
    });
}

document.getElementById('is_mobile').value = isMobile() ? "True" : "False";
console.log("is_mobile is", document.getElementById('is_mobile').value)