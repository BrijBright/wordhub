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
                icon.classList.remove('bi-copy');
                icon.classList.add('bi-check');
                text.style.visibility = 'visible';
                const wordCell = row.querySelectorAll('td')[0];
                wordCell.classList.add('copy-highlight');
                setTimeout(() => wordCell.classList.remove('copy-highlight'), 800);
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

            icon.classList.add('speak-animate');
            setTimeout(() => icon.classList.remove('speak-animate'), 500);

            const wordCell = row.querySelectorAll('td')[0];
            wordCell.classList.add('copy-highlight');
            setTimeout(() => wordCell.classList.remove('copy-highlight'), 800);

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

    // ---------------- MARK REVISED ----------------
    document.querySelectorAll('.mark-revised-icon').forEach(icon => {
        icon.addEventListener('click', () => {
            handleWordAction(icon, 'mark_revised', { increment: 1 }, 'bi-check-square-fill');
        });
    });

    // ---------------- MARK NEEDS IMPROVEMENT ----------------
    document.querySelectorAll('.improvement-icon').forEach(icon => {
        icon.addEventListener('click', () => {
            const row = icon.closest('tr');
            const wordId = row.getAttribute('data-word-id');
            const masteredIcon = row.querySelector('.mastered-icon');

            const isActive = icon.classList.contains('bi-exclamation-triangle-fill');

            // --- TOGGLE UI ---
            if (isActive) {
                // Turning OFF
                icon.classList.remove('bi-exclamation-triangle-fill');
                icon.classList.add('bi-exclamation-triangle');
            } else {
                // Turning ON
                icon.classList.remove('bi-exclamation-triangle');
                icon.classList.add('bi-exclamation-triangle-fill');

                // Turn OFF mastered if on
                masteredIcon.classList.remove('bi-star-fill');
                masteredIcon.classList.add('bi-star');
            }

            // --- SEND TO BACKEND ---
            fetch(`/api/words/${wordId}/mark_improvement/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({})
            })
                .then(res => res.json())
                .then(data => console.log("Improvement updated:", data))
                .catch(err => console.error(err));
        });
    });



    // ---------------- MARK MASTERED ----------------
    document.querySelectorAll('.mastered-icon').forEach(icon => {
        icon.addEventListener('click', () => {
            const row = icon.closest('tr');
            const wordId = row.getAttribute('data-word-id');
            const improvementIcon = row.querySelector('.improvement-icon');

            const isActive = icon.classList.contains('bi-star-fill');

            // --- TOGGLE UI ---
            if (isActive) {
                // Turning OFF
                icon.classList.remove('bi-star-fill');
                icon.classList.add('bi-star');
            } else {
                // Turning ON
                icon.classList.remove('bi-star');
                icon.classList.add('bi-star-fill');

                // Turn OFF improvement if ON
                improvementIcon.classList.remove('bi-exclamation-triangle-fill');
                improvementIcon.classList.add('bi-exclamation-triangle');
            }

            // --- SEND TO BACKEND ---
            fetch(`/api/words/${wordId}/toggle_mastered/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({})
            })
                .then(res => res.json())
                .then(data => console.log("Mastered updated:", data))
                .catch(err => console.error(err));
        });
    });


    // ---------------- GENERIC WORD ACTION HANDLER ----------------
    function handleWordAction(icon, action, payload = {}, highlightClass = '', highlightColor = '') {
        const row = icon.closest('tr');
        const wordId = row.getAttribute('data-word-id');

        // Animate icon if highlightClass is provided
        if (highlightClass) {
            icon.classList.add(highlightClass);
            setTimeout(() => icon.classList.remove(highlightClass), 500);
        }

        // Optional: change color temporarily
        if (highlightColor) {
            const originalColor = icon.style.color;
            icon.style.color = highlightColor;
            setTimeout(() => icon.style.color = originalColor, 800);
        }

        // Send POST request to backend API
        fetch(`/api/words/${wordId}/${action}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(payload)
        })
            .then(res => res.json())
            .then(data => console.log(`${action} success:`, data))
            .catch(err => console.error(err));
    }

    // ---------------- CSRF HELPER ----------------
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
});