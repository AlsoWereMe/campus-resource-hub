// 由 contracts/<api>/openapi.yaml 生成 TypeScript 类型到 src/shell/api/types/。
// 契约变化后运行：pnpm gen:api（make contracts 会自动运行）。
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import openapiTS, { astToString } from "openapi-typescript";

const here = dirname(fileURLToPath(import.meta.url));
const contracts = join(here, "..", "..", "..", "contracts");
const out = join(here, "..", "src", "shell", "api", "types");
const apis = ["iam", "space", "notify", "audit", "m1", "m2", "m3"];

mkdirSync(out, { recursive: true });
for (const api of apis) {
  const source = readFileSync(join(contracts, api, "openapi.yaml"), "utf8");
  const ast = await openapiTS(source);
  const header = `// 由 contracts/${api}/openapi.yaml 生成，请勿手改。重新生成：pnpm gen:api\n`;
  writeFileSync(join(out, `${api}.ts`), header + astToString(ast));
  console.log(`已生成 src/shell/api/types/${api}.ts`);
}
