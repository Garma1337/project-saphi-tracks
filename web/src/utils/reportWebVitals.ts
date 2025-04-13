import {onLCP, onINP, onCLS, onFID, onFCP, onTTFB} from 'web-vitals';

export default function reportWebVitals() {
    onCLS(console.log);
    onINP(console.log);
    onLCP(console.log);
    onFID(console.log);
    onFCP(console.log);
    onTTFB(console.log);
}
