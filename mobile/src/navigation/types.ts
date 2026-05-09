// Navigation type definitions for type-safe routing

export type RootStackParamList = {
  Tabs: undefined;
  SystemDetail: { systemId: string };
};

export type TabParamList = {
  Overview: undefined;
  Alerts: undefined;
};
