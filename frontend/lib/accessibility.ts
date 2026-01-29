/**
 * Accessibility utilities for the Course Companion FTE application
 */

// Focus trap for modal dialogs
export function trapFocus(element: HTMLElement, firstFocusable?: HTMLElement) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ) as NodeListOf<HTMLElement>;

  const firstElement = firstFocusable || focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey && document.activeElement === firstElement) {
      lastElement.focus();
      e.preventDefault();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      firstElement.focus();
      e.preventDefault();
    }
  };

  element.addEventListener('keydown', handleKeyDown);

  // Clean up function
  return () => element.removeEventListener('keydown', handleKeyDown);
}

// Announce messages to screen readers
export function announce(message: string, priority: 'polite' | 'assertive' = 'polite') {
  const announcement = document.createElement('div');
  const id = `announcement-${Date.now()}`;

  announcement.setAttribute('id', id);
  announcement.setAttribute('aria-live', priority);
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';
  announcement.textContent = message;

  document.body.appendChild(announcement);

  // Clean up after announcement
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
}

// Manage focus when components mount/unmount
export function manageFocusOnMount(element: HTMLElement | null) {
  if (element) {
    element.focus();
  }
}

// Scroll to element with smooth behavior
export function scrollToElement(selector: string, options?: ScrollIntoViewOptions) {
  const element = document.querySelector(selector);
  if (element) {
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
      ...options
    });
  }
}

// Check if high contrast mode is enabled
export function isHighContrastMode(): boolean {
  if (typeof window === 'undefined') return false;

  const testElement = document.createElement('div');
  testElement.style.border = '1px solid transparent';
  document.body.appendChild(testElement);

  const computedStyle = window.getComputedStyle(testElement);
  const isHighContrast = computedStyle.borderTopColor !== computedStyle.borderRightColor;

  document.body.removeChild(testElement);

  return isHighContrast;
}

// Toggle reduced motion preference
export function prefersReducedMotion(): boolean {
  if (typeof window === 'undefined') return false;

  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

// Update document title with accessibility considerations
export function updateDocumentTitle(title: string) {
  document.title = `${title} - Course Companion FTE`;
}

// Add ARIA attributes to dynamic content
export function addAriaAttributes(element: HTMLElement, attributes: Record<string, string>) {
  Object.entries(attributes).forEach(([key, value]) => {
    element.setAttribute(key, value);
  });
}