
export default function Logo({ className = "h-8 w-auto" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 280 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-label="Neumaticopedia"
    >
      {/* Tire icon */}
      <circle cx="24" cy="24" r="22" stroke="#2563eb" strokeWidth="3" fill="none" />
      <circle cx="24" cy="24" r="14" stroke="#2563eb" strokeWidth="2" fill="none" />
      <circle cx="24" cy="24" r="5" fill="#2563eb" />
      {/* Tread pattern */}
      <line x1="24" y1="2" x2="24" y2="10" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" />
      <line x1="24" y1="38" x2="24" y2="46" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" />
      <line x1="2" y1="24" x2="10" y2="24" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" />
      <line x1="38" y1="24" x2="46" y2="24" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" />
      <line x1="8.3" y1="8.3" x2="13.9" y2="13.9" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" />
      <line x1="34.1" y1="34.1" x2="39.7" y2="39.7" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" />
      <line x1="39.7" y1="8.3" x2="34.1" y2="13.9" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" />
      <line x1="13.9" y1="34.1" x2="8.3" y2="39.7" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" />
      {/* Text */}
      <text x="56" y="33" fill="#1a2332" fontFamily="Inter, system-ui, sans-serif" fontWeight="700" fontSize="26">
        Neumático
      </text>
      <text x="215" y="33" fill="#2563eb" fontFamily="Inter, system-ui, sans-serif" fontWeight="700" fontSize="26">
        pedia
      </text>
    </svg>
  );
}
