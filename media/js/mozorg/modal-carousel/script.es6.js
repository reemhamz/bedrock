/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Setting up directional buttons to add to modal. This could be done within Protocol

const modalNextButtonFragment = `<div class="c-modal-next">
        <button type="button" class="c-modal-button-next" title="Next">
            Next
        </button>
    </div>`;

const modalPrevButtonFragment = `<div class="c-modal-prev">
        <button type="button" class="c-modal-button-prev" title="Previous">
            Previous
        </button>
    </div>`;

// This function is a boilerplate for when we create modals on bedrock using protocol. The objects and functions mentioned were already created here: https://github.com/mozilla/protocol/blob/main/assets/js/protocol/protocol-modal.js

function triggerCarousel(carousel) {
    // If we call the triggerCarousel function without passing a variable containing the elements we're looking for, then it will throw this error
    if (!carousel) {
        throw new Error('No carousel found!');
    }

    function showContent(el) {
        if (!el) {
            // console.info('no content to show');
            return;
        }
        // console.log(el);
    }

    // Creating a variable to be placed in the triggerCarousel() function, which looks into the variable created and creates an array from the element mentioned in the variable
    const modalAnchor = Array.from(carousel.querySelectorAll('.modal-button'));

    modalAnchor.map((item, index) => {
        item.addEventListener(
            'click',
            function (e) {
                e.preventDefault();
                // console.log(item, index);

                const content = e.target.nextElementSibling;
                const currentContainer = e.target.parentElement;
                const nextContainer = currentContainer.nextElementSibling;
                const prevContainer = currentContainer.previousElementSibling;

                Mzp.Modal.createModal(item, content, {
                    title: 'You opened the modal'
                });

                // Adding directional buttons to be close to close button. This could be done within Protocol
                const modalCloseButton =
                    document.querySelector('.mzp-c-modal-close');
                modalCloseButton.insertAdjacentHTML(
                    'beforebegin',
                    modalNextButtonFragment
                );
                modalCloseButton.insertAdjacentHTML(
                    'beforebegin',
                    modalPrevButtonFragment
                );

                const nextButton = document.querySelector('.c-modal-next');
                const prevButton = document.querySelector('.c-modal-prev');

                // Adding event listeners for the directional buttons
                nextButton.addEventListener('click', function () {
                    // Mzp.Modal.createModal()
                    console.log(nextContainer);
                    // console.log('before change', currentContainer);
                    currentContainer = nextContainer;
                    // console.log('after change', currentContainer);
                });

                prevButton.addEventListener('click', function () {
                    // console.log('before change', currentContainer);
                    currentContainer = prevContainer;
                    // console.log('after change', currentContainer);
                });
            },
            false
        );
    });
}

const carouselWrapper = triggerCarousel(
    document.querySelector('.mzp-c-modal-carousel')
);
