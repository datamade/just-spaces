import { helloWorld } from "../../src/js/helloworld";

// Instruct JSHint to ignore the Jasmine global objects (e.g. 'describe', 'it')
// that appear to be undefined.
/* jshint undef: false */
describe("Test helloWorld", function() {
  it("returns true", function () {
      var result = helloWorld();
      expect(result).toBe(true);
  });
});
