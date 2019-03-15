import { helloWorld } from "../../src/js/helloworld";

/* jshint undef: false */
describe("Test helloWorld", function() {
  it("returns true", function () {
      var result = helloWorld();
      expect(result).toBe(true);
  });
});
