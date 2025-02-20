interface Config {
    DEBUG: boolean;
    TTS_SPEED: number;
    THRESHOLDING: number;
}

export const config: Config = $state({
    DEBUG: false,
    TTS_SPEED: 0,
    THRESHOLDING: 0,
});

export const fetchConfig = async () => {
    const response = await fetch("http://localhost:5001/api/settings");
    const data = await response.json();
    for (const key in data) {
        if (key in config) {
            (config as any)[key] = data[key];
        }
    }
};

export const updateConfig = async () => {
    const response = await fetch("http://localhost:5001/api/settings", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(config),
    });
};
