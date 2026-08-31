type DoodleProps = {
  className?: string;
  strokeWidth?: number;
  color?: string;
};

/* Hand-drawn wavy underline / squiggle strokes */
export function Squiggle({ className, color = "#ff4126", strokeWidth = 3 }: DoodleProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 200 20"
      fill="none"
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      <path
        d="M2 12 C 22 3, 38 16, 58 9 S 96 4, 116 11 S 156 6, 178 11 C 188 14, 194 11, 198 9"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        fill="none"
      />
    </svg>
  );
}

/* A wobbly circle drawn in one go — the signature doodle frame */
export function WobbleCircle({ className, color = "#1f5f4b", strokeWidth = 3 }: DoodleProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 120 120"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M14 60 C14 34, 34 12, 60 12 C88 12, 106 34, 106 60 C106 88, 86 106, 60 106 C32 106, 13 88, 14 60 C14.5 42, 30 26, 48 24 C66 22, 82 36, 80 54 C78 70, 66 82, 50 80 C36 78, 28 64, 32 50"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        fill="none"
      />
    </svg>
  );
}

/* Little hand-drawn arrow */
export function Arrow({ className, color = "#ff4126", strokeWidth = 3 }: DoodleProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 120 60"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M8 8 C 40 20, 70 40, 104 50"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
      <path
        d="M96 42 C 100 48, 104 50, 112 51 M96 42 C 102 38, 106 38, 112 40"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        fill="none"
      />
    </svg>
  );
}

/* Spiral doodle */
export function Spiral({ className, color = "#0a0a07", strokeWidth = 3 }: DoodleProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 80 80"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M40 40 C 46 34, 52 38, 50 46 C 48 54, 36 58, 28 52 C 20 44, 24 30, 36 24 C 50 17, 62 26, 62 38 C 62 52, 50 62, 38 62"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
    </svg>
  );
}

/* Hand-drawn sparkle / burst */
export function Sparkle({ className, color = "#ff4126", strokeWidth = 3 }: DoodleProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 60 60"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M30 6 C31 20, 30 26, 33 30 M30 6 C29 20, 30 26, 27 30 M30 54 C31 40, 30 34, 33 30 M30 54 C29 40, 30 34, 27 30 M6 30 C20 31, 26 30, 30 27 M6 30 C20 29, 26 30, 30 33 M54 30 C40 31, 34 30, 30 27 M54 30 C40 29, 34 30, 30 33"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
      <circle cx="30" cy="30" r="2.5" fill={color} />
    </svg>
  );
}

/* A hand-drawn plant / branch doodle for decor */
export function Plant({ className, color = "#1f5f4b", strokeWidth = 3 }: DoodleProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 80 100"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M40 96 C40 78, 40 60, 40 44"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
      <path
        d="M40 66 C 30 58, 24 52, 22 42 M40 70 C 32 66, 24 62, 18 58"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
      <path
        d="M40 50 C 48 42, 54 36, 56 28 M40 56 C 48 48, 52 42, 52 34"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
      <ellipse cx="22" cy="40" rx="2.5" ry="4" fill={color} />
      <ellipse cx="56" cy="27" rx="2.5" ry="4" fill={color} />
    </svg>
  );
}
