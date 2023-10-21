const nodeName = "textNode";
const component = `
<div>
  <div class="title-box text"><i class="fas fa-paragraph"></i>Text node</div>
  <div class="box">
    <p>Enter Text to display</p>
  <textarea df-text></textarea>
  </div>
</div>
`;

const menuIcon = `<div
class="drag-drawflow"
draggable="true"
ondragstart="drag(event)"
data-node="${nodeName}">
<i class="fas fa-paragraph"></i><span> Text Node!</span>
<div id="description_text" style="display: none;">
    <p>Text to be displayed by the Chatbot</p>
</div>
</div>`
;

export const initTextNode = () => {
  const menu = document.getElementById("menu-container");
  menu.insertAdjacentHTML("beforeend", menuIcon);
  // Add event listener to show description when dropdown button is clicked
  var descriptionDiv = document.getElementById("description_text");

    // Get a reference to the element you want to click on
    var element = document.querySelector(`div.drag-drawflow[data-node="${nodeName}"]`);

    // Add a click event listener to the element
    element.addEventListener("click", function () {
        // Toggle the display of the description div
        if (descriptionDiv.style.display === "none") {
            descriptionDiv.style.display = "block";
        } else {
            descriptionDiv.style.display = "none";
        }
    });
};

export const addTextNode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { text: "" },
    component
  );
};
