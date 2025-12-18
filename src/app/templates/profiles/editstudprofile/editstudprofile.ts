document.addEventListener('DOMContentLoaded', function (): void {
    const navSteps = document.querySelectorAll('.edit-student-profile-step');
    const formSteps = document.querySelectorAll('.edit-student-profile-form__step');

    function showStep(stepId: string): void {
        formSteps.forEach(step => step.classList.remove('edit-student-profile-form__step--active'));
        navSteps.forEach(step => step.classList.remove('edit-student-profile-step--active'));

        const stepElement = document.getElementById(`step-${stepId}`);
        const navStepElement = document.querySelector(`.edit-student-profile-step[data-step="${stepId}"]`);

        if (stepElement) {
            stepElement.classList.add('edit-student-profile-form__step--active');
        }

        if (navStepElement) {
            navStepElement.classList.add('edit-student-profile-step--active');
        }
    }

    navSteps.forEach(step => {
        step.addEventListener('click', function (this: HTMLElement, e: Event) {
            e.preventDefault();
            const stepId = this.getAttribute('data-step');
            if (stepId) {
                showStep(stepId);
            }
        });
    });
});
