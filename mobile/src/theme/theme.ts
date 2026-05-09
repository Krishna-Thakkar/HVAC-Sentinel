import { DarkTheme } from '@react-navigation/native';

export const colors = {
  background: '#0d1117',
  surface: '#161b22',
  surfaceElevated: '#21262d',
  border: '#30363d',
  text: {
    primary: '#e6edf3',
    secondary: '#8b949e',
    muted: '#484f58',
  },
  severity: {
    critical: '#f85149',
    warning: '#d29922',
    normal: '#3fb950',
    info: '#58a6ff',
  },
  accent: '#58a6ff',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const typography = {
  sizes: {
    xs: 11,
    sm: 13,
    md: 15,
    lg: 17,
    xl: 20,
    xxl: 24,
  },
  weights: {
    regular: '400' as const,
    medium: '500' as const,
    semibold: '600' as const,
    bold: '700' as const,
  },
};

export const theme = {
  colors,
  spacing,
  typography,
  navigation: {
    ...DarkTheme,
    colors: {
      ...DarkTheme.colors,
      background: colors.background,
      card: colors.surface,
      text: colors.text.primary,
      border: colors.border,
      primary: colors.accent,
    },
  },
};
