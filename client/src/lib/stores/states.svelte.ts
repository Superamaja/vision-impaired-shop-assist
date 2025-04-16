interface Config {
  DEBUG: boolean;
  TTS_SPEED: number;
  THRESHOLDING: number;
  TTS_OCR_TEMPLATE: string;
  TTS_BARCODE_FOUND_TEMPLATE: string;
  TTS_BARCODE_NOT_FOUND_TEMPLATE: string;
}

export const config: Config = $state({
  DEBUG: false,
  TTS_SPEED: 0,
  THRESHOLDING: 0,
  TTS_OCR_TEMPLATE: "",
  TTS_BARCODE_FOUND_TEMPLATE: "",
  TTS_BARCODE_NOT_FOUND_TEMPLATE: "",
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
