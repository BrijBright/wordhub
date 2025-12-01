document.addEventListener('DOMContentLoaded', () => {

    // ---------------- INITIALIZE TOOLTIP ----------------
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(el => new bootstrap.Tooltip(el));

    // Optionally disable tooltip if title is empty
    document.querySelectorAll('.word-cell').forEach(td => {
        if (!td.getAttribute('title')) {
            td.removeAttribute('data-bs-toggle');
        }
    });

    // ---------------- COPY FUNCTIONALITY ----------------
    document.querySelectorAll('.copy-icon').forEach(icon => {
        icon.addEventListener('click', () => {
            const row = icon.closest('tr');
            const word = row.querySelectorAll('td')[0].textContent.trim();
            const text = row.querySelector('.copy-text');

            navigator.clipboard.writeText(word).then(() => {
                // 1. Change icon → tick
                icon.classList.remove('bi-copy');
                icon.classList.add('bi-check');

                // 2. Show "Copied!" text
                text.style.visibility = 'visible';

                // 3. Animate word cell (highlight)
                const wordCell = row.querySelectorAll('td')[0];
                wordCell.classList.add('copy-highlight');
                setTimeout(() => wordCell.classList.remove('copy-highlight'), 800);

                // 4. Revert icon and text
                setTimeout(() => {
                    icon.classList.remove('bi-check');
                    icon.classList.add('bi-copy');
                    text.style.visibility = 'hidden';
                }, 1500);
            });
        });
    });

    // ---------------- SPEAKER FUNCTIONALITY ----------------
    document.querySelectorAll('.speak-icon').forEach(icon => {
        icon.addEventListener('click', () => {
            const row = icon.closest('tr');
            const word = row.querySelectorAll('td')[0].textContent.trim();
            const url = `https://youglish.com/pronounce/${encodeURIComponent(word)}/english`;

            // Animate icon
            icon.classList.add('speak-animate');
            setTimeout(() => icon.classList.remove('speak-animate'), 500);

            // Highlight word cell
            const wordCell = row.querySelectorAll('td')[0];
            wordCell.classList.add('copy-highlight');
            setTimeout(() => wordCell.classList.remove('copy-highlight'), 800);

            // Open YouGlish in new tab
            window.open(url, '_blank', 'noopener,noreferrer');
        });
    });

    // ---------------- DEFINITION FUNCTIONALITY ----------------
    document.querySelectorAll('.definition-icon').forEach(icon => {
        icon.addEventListener('click', () => {
            const row = icon.closest('tr');
            const word = row.querySelectorAll('td')[0].textContent.trim();
            const url = `https://www.dictionary.com/browse/${encodeURIComponent(word)}`;
            window.open(url, '_blank', 'noopener,noreferrer');
        });
    });

});


document.addEventListener('DOMContentLoaded', () => {

    // Event listener for "Mark Revised"
    document.querySelectorAll('.mark-revised-icon').forEach(icon => {
        icon.addEventListener('click', () => {
            const row = icon.closest('tr');
            const wordId = row.getAttribute('data-word-id');
            const countCell = row.querySelector('.revised-count');

            // Increment revised count in UI
            let count = parseInt(countCell.textContent);
            count += 1;
            countCell.textContent = count;

            // Optionally animate icon
            icon.classList.add('bi-check-square-fill');  // filled check
            setTimeout(() => icon.classList.remove('bi-check-square-fill'), 500);

            // Update DB via AJAX
            fetch(`/api/words/${wordId}/mark_revised/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ increment: 1 })
            })
                .then(res => res.json())
                .then(data => console.log('Updated:', data))
                .catch(err => console.error(err));
        });
    });

});

// CSRF helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// document.querySelectorAll('.row').forEach(el => {
//     el.addEventListener('mouseenter', () => el.classList.add('bg-primary', 'text-white'));
//     el.addEventListener('mouseleave', () => el.classList.remove('bg-primary', 'text-white'));
// });