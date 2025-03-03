interface ImportMetaEnv {
    VITE_BASE_MAP_URL: string;
    readonly VITE_API_HOST: string;
    readonly VITE_MODE: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}