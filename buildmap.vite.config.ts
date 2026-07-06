import 'dotenv/config';
import fs from "fs";
import path from "path";
import { defineConfig, Plugin } from "vite";
import { getMaps, getMapsOptimizers, getMapsScripts, LogLevel, OptimizeOptions } from "wa-map-optimizer-vite";

// getMaps()/getMapsOptimizers() only process .tmj files (e.g. office_base.tmj,
// townhall_base.tmj). Our actual rooms (lobby.wam, floor_alpha.wam,
// floor_bravo.wam, floor_charlie.wam, townhall.wam) are hand-built .wam files
// referencing those base .tmj layouts — they were never copied into dist/, so
// upload-wa-map never uploaded them and START_ROOM_URL pointed at a 404.
// This copies every top-level .wam file into the build output so any room
// added in the future is picked up automatically too.
function copyRoomWamFiles(): Plugin {
    let outDir = "dist";
    return {
        name: "copy-room-wam-files",
        configResolved(config) {
            outDir = config.build.outDir;
        },
        closeBundle() {
            const root = process.cwd();
            for (const file of fs.readdirSync(root)) {
                if (file.endsWith(".wam")) {
                    fs.copyFileSync(path.join(root, file), path.join(outDir, file));
                }
            }
        },
    };
}

const maps = getMaps();

let optimizerOptions: OptimizeOptions = {
    logs: process.env.LOG_LEVEL && process.env.LOG_LEVEL in LogLevel ? LogLevel[process.env.LOG_LEVEL] : LogLevel.NORMAL,
};

if (process.env.TILESET_OPTIMIZATION && process.env.TILESET_OPTIMIZATION === "true") {
    const qualityMin = process.env.TILESET_OPTIMIZATION_QUALITY_MIN ? parseInt(process.env.TILESET_OPTIMIZATION_QUALITY_MIN) : 0.9;
    const qualityMax = process.env.TILESET_OPTIMIZATION_QUALITY_MAX ? parseInt(process.env.TILESET_OPTIMIZATION_QUALITY_MAX) : 1;

    optimizerOptions.output = {
        tileset: {
            compress: {
                quality: [qualityMin, qualityMax],
            }
        }
    }
}

export default defineConfig({
    base: "./",
    build: {
        sourcemap: true,
        rollupOptions: {
            input: {
                ...getMapsScripts(maps),
            },
        },
    },
    preview: {
        cors: true,
    },
    plugins: [
        ...getMapsOptimizers(maps, optimizerOptions),
        copyRoomWamFiles(),
    ],
});
