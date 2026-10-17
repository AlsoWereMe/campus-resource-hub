import { expect, test } from "@playwright/test";

// 冒烟：演示账号登录后看到按权限生成的菜单（IAM-AUTH-01）。
test("学生登录后看到找座位菜单", async ({ page }) => {
  await page.goto("/login/");
  await page.getByLabel("学号 / 工号").fill("student1");
  await page.getByLabel("口令").fill("Passw0rd!");
  await page.getByRole("button", { name: "登录" }).click();
  await expect(page.getByRole("link", { name: "找座位" })).toBeVisible();
  await expect(page.getByRole("link", { name: "运营看板" })).toHaveCount(0);
});

test("错误口令提示统一的错误信息", async ({ page }) => {
  await page.goto("/login/");
  await page.getByLabel("学号 / 工号").fill("student1");
  await page.getByLabel("口令").fill("wrong-password");
  await page.getByRole("button", { name: "登录" }).click();
  await expect(page.getByRole("alert")).toHaveText("用户名或密码错误");
});
