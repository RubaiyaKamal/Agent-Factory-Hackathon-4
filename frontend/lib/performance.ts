/**
 * Performance utilities for the Course Companion FTE application
 */

// Debounce function to limit function calls
export function debounce<T extends (...args: any[]) => any>(func: T, wait: number) {
  let timeout: NodeJS.Timeout;
  return function executedFunction(...args: Parameters<T>): void {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Throttle function to ensure function is called at most once per interval
export function throttle<T extends (...args: any[]) => any>(func: T, limit: number) {
  let inThrottle: boolean;
  return function throttledFunction(...args: Parameters<T>): void {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
  };
}

// Memoize function to cache expensive computations
export function memoize<T extends (...args: any[]) => any>(func: T) {
  const cache = new Map<string, ReturnType<T>>();
  return function memoizedFunction(...args: Parameters<T>): ReturnType<T> {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key)!;
    }
    const result = func(...args);
    cache.set(key, result);
    return result;
  };
}

// Lazy load images
export function lazyLoadImage(image: HTMLImageElement) {
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement;
          img.src = img.dataset.src || '';
          img.classList.remove('lazy');
          imageObserver.unobserve(img);
        }
      });
    });

    imageObserver.observe(image);
  } else {
    // Fallback for browsers that don't support IntersectionObserver
    const src = image.dataset.src;
    if (src) {
      image.src = src;
    }
  }
}

// Virtual scrolling helper
export interface VirtualScrollOptions {
  itemHeight: number;
  containerHeight: number;
  itemCount: number;
}

export function calculateVisibleRange(scrollTop: number, options: VirtualScrollOptions) {
  const { itemHeight, containerHeight, itemCount } = options;
  const itemsPerScreen = Math.ceil(containerHeight / itemHeight);
  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - itemsPerScreen);
  const endIndex = Math.min(itemCount - 1, startIndex + itemsPerScreen * 3);

  return {
    startIndex,
    endIndex,
    offset: startIndex * itemHeight
  };
}

// Performance measurement utility
export class PerformanceTimer {
  private marks: Map<string, number> = new Map();

  start(label: string) {
    this.marks.set(label, performance.now());
  }

  end(label: string) {
    const start = this.marks.get(label);
    if (start !== undefined) {
      const duration = performance.now() - start;
      this.marks.delete(label);
      return duration;
    }
    return null;
  }

  measure<T>(label: string, fn: () => T): T {
    this.start(label);
    const result = fn();
    const duration = this.end(label);
    if (duration !== null) {
      console.log(`${label}: ${duration.toFixed(2)}ms`);
    }
    return result;
  }
}

// Memory cleanup utility
export function cleanupMemory(obj: any) {
  // Clear any timers
  if (obj.__timers) {
    obj.__timers.forEach((timer: number) => clearTimeout(timer));
    obj.__timers = [];
  }

  // Clear any intervals
  if (obj.__intervals) {
    obj.__intervals.forEach((interval: number) => clearInterval(interval));
    obj.__intervals = [];
  }

  // Clear any event listeners
  if (obj.__eventListeners) {
    obj.__eventListeners.forEach(({ element, event, handler }: { element: EventTarget, event: string, handler: EventListener }) => {
      element.removeEventListener(event, handler);
    });
    obj.__eventListeners = [];
  }
}

// Lazy component loader
export function lazyImport<T>(importFn: () => Promise<{ default: T }>) {
  return importFn();
}

// Check if browser supports performance API
export function supportsPerformanceAPI(): boolean {
  return typeof performance !== 'undefined' && !!performance.mark && !!performance.measure;
}

// Measure and log performance metrics
export function measurePerformance(metricName: string, startMark: string, endMark: string) {
  if (supportsPerformanceAPI()) {
    performance.measure(metricName, startMark, endMark);
    const measure = performance.getEntriesByName(metricName)[0];
    if (measure) {
      console.log(`${metricName}: ${measure.duration.toFixed(2)}ms`);
      return measure.duration;
    }
  }
  return 0;
}